from datetime import datetime

from bottle import template

from app.models.atendimento import Atendimento
from app.models.procedimento import Procedimento
from app.models.repositorio import RepositorioProcedimentos, RepositorioAtendimentos
from app.models.classificador import ClassificadorPalavrasChave
from app.models.analisador import AnalisadorFaturamento


class Application():

    def __init__(self):
        self.pages = {
            'index': self.index,
            'atendimentos': self.atendimentos_lista,
            'atendimento_novo': self.atendimento_novo,
            'atendimento_detalhe': self.atendimento_detalhe,
            'atendimento_editar': self.atendimento_editar,
            'procedimentos': self.procedimentos_lista,
            'procedimento_novo': self.procedimento_novo,
            'procedimento_editar': self.procedimento_editar
        }
        self.procedimentos = RepositorioProcedimentos()
        self.atendimentos = RepositorioAtendimentos()
        self.analisador = AnalisadorFaturamento()


    def render(self, page, parametro=None):
        content = self.pages.get(page, self.helper)
        if parametro is None:
            return content()
        return content(parametro)


    def helper(self, parametro=None):
        return template('app/views/html/helper')


    def index(self):
        return template('app/views/html/index')


    # ------------------------------------------------------------------
    # Funções de apoio

    def criar_classificador(self):
        # Para trocar de classificador no futuro, só esta linha muda
        return ClassificadorPalavrasChave(self.procedimentos.listar())

    def analisar(self, atendimento):
        classificador = self.criar_classificador()
        sugestoes = classificador.sugerir(atendimento.texto)
        nao_faturados, sem_evidencia = self.analisador.comparar(sugestoes, atendimento.faturados)
        return sugestoes, nao_faturados, sem_evidencia

    def descrever(self, codigo):
        # Código -> {'codigo': ..., 'nome': ...}, para mostrar na página
        procedimento = self.procedimentos.buscar_por_id(codigo)
        if procedimento is None:
            return {'codigo': codigo, 'nome': '(fora do catálogo)'}
        return {'codigo': codigo, 'nome': procedimento.nome}

    def separar_palavras(self, texto):
        # "usg, ultrassom , abdome" -> ['usg', 'ultrassom', 'abdome']
        palavras = []
        for pedaco in texto.split(','):
            pedaco = pedaco.strip()
            if pedaco != '':
                palavras.append(pedaco)
        return palavras


    # ------------------------------------------------------------------
    # Páginas de atendimentos

    def atendimentos_lista(self):
        linhas = []
        # reversed: o atendimento mais novo aparece primeiro
        for atendimento in reversed(self.atendimentos.listar()):
            sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)
            linhas.append({
                'atendimento': atendimento,
                'alertas': len(nao_faturados),
                'avisos': len(sem_evidencia)
            })
        return template('app/views/html/atendimentos', linhas=linhas)

    def atendimento_novo(self):
        return template('app/views/html/atendimento_form',
                        titulo='Novo atendimento',
                        acao='/atendimentos',
                        atendimento=None,
                        procedimentos=self.procedimentos.listar())

    def atendimento_editar(self, id):
        atendimento = self.atendimentos.buscar_por_id(id)
        if atendimento is None:
            return template('app/views/html/nao_encontrado', mensagem='Atendimento não encontrado.')
        return template('app/views/html/atendimento_form',
                        titulo='Editar atendimento nº ' + str(id),
                        acao='/atendimentos/' + str(id) + '/editar',
                        atendimento=atendimento,
                        procedimentos=self.procedimentos.listar())

    def atendimento_detalhe(self, id):
        atendimento = self.atendimentos.buscar_por_id(id)
        if atendimento is None:
            return template('app/views/html/nao_encontrado', mensagem='Atendimento não encontrado.')

        sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)

        faturados = []
        for codigo in atendimento.faturados:
            faturados.append(self.descrever(codigo))

        sem_evidencia_descritos = []
        for codigo in sem_evidencia:
            sem_evidencia_descritos.append(self.descrever(codigo))

        # Palavras que o JavaScript vai destacar no texto
        palavras = []
        for sugestao in sugestoes:
            for palavra in sugestao.palavras_encontradas:
                if palavra not in palavras:
                    palavras.append(palavra)

        return template('app/views/html/atendimento_detalhe',
                        atendimento=atendimento,
                        sugestoes=sugestoes,
                        faturados=faturados,
                        nao_faturados=nao_faturados,
                        sem_evidencia=sem_evidencia_descritos,
                        palavras=palavras)


    # Ações (chamadas pelas rotas POST)

    def criar_atendimento(self, texto, faturados):
        novo_id = self.atendimentos.proximo_id()
        data = datetime.now().strftime('%d/%m/%Y %H:%M')
        atendimento = Atendimento(novo_id, texto, faturados, data)
        self.atendimentos.adicionar(atendimento)
        return novo_id

    def editar_atendimento(self, id, texto, faturados):
        antigo = self.atendimentos.buscar_por_id(id)
        if antigo is None:
            return False
        # A data do cadastro continua a mesma
        novo = Atendimento(id, texto, faturados, antigo.data)
        return self.atendimentos.atualizar(novo)

    def excluir_atendimento(self, id):
        return self.atendimentos.remover(id)


    # ------------------------------------------------------------------
    # Páginas do catálogo de procedimentos

    def procedimentos_lista(self):
        return template('app/views/html/procedimentos',
                        procedimentos=self.procedimentos.listar())

    def procedimento_novo(self, erro=None):
        return template('app/views/html/procedimento_form',
                        titulo='Novo procedimento',
                        acao='/procedimentos',
                        procedimento=None,
                        erro=erro)

    def procedimento_editar(self, codigo):
        procedimento = self.procedimentos.buscar_por_id(codigo)
        if procedimento is None:
            return template('app/views/html/nao_encontrado', mensagem='Procedimento não encontrado.')
        return template('app/views/html/procedimento_form',
                        titulo='Editar procedimento',
                        acao='/procedimentos/' + codigo + '/editar',
                        procedimento=procedimento,
                        erro=None)


    # Ações (chamadas pelas rotas POST)

    def criar_procedimento(self, codigo, nome, palavras_texto):
        # Devolve uma mensagem de erro, ou None se deu certo
        codigo = codigo.strip()
        nome = nome.strip()
        palavras = self.separar_palavras(palavras_texto)
        if codigo == '' or nome == '' or len(palavras) == 0:
            return 'Preencha o código, o nome e pelo menos uma palavra-chave.'
        if self.procedimentos.buscar_por_id(codigo) is not None:
            return 'Já existe um procedimento com o código ' + codigo + '.'
        self.procedimentos.adicionar(Procedimento(codigo, nome, palavras))
        return None

    def editar_procedimento(self, codigo, nome, palavras_texto):
        nome = nome.strip()
        palavras = self.separar_palavras(palavras_texto)
        if nome == '' or len(palavras) == 0:
            return False
        return self.procedimentos.atualizar(Procedimento(codigo, nome, palavras))

    def excluir_procedimento(self, codigo):
        return self.procedimentos.remover(codigo)
