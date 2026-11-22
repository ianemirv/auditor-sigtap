from datetime import datetime

from bottle import template

from app.models.atendimento import Atendimento
from app.models.procedimento import Procedimento
from app.models.repositorio import RepositorioProcedimentos, RepositorioAtendimentos
from app.models.repositorio import RepositorioUsuarios
from app.models.classificador import ClassificadorPalavrasChave
from app.models.analisador import AnalisadorFaturamento
from app.models.usuario import novo_usuario
from app.models.notificador import NotificadorAuditoria


class Application():

    def __init__(self):
        self.pages = {
            'index': self.index,
            'login': self.login_pagina,
            'painel': self.painel,
            'acesso_negado': self.acesso_negado,
            'atendimentos': self.atendimentos_lista,
            'atendimento_novo': self.atendimento_novo,
            'atendimento_detalhe': self.atendimento_detalhe,
            'atendimento_editar': self.atendimento_editar,
            'procedimentos': self.procedimentos_lista,
            'procedimento_novo': self.procedimento_novo,
            'procedimento_editar': self.procedimento_editar,
            'usuarios': self.usuarios_lista,
            'usuario_novo': self.usuario_novo,
            'usuario_editar': self.usuario_editar,
            'auditoria': self.auditoria
        }
        self.procedimentos = RepositorioProcedimentos()
        self.atendimentos = RepositorioAtendimentos()
        self.usuarios = RepositorioUsuarios()
        self.analisador = AnalisadorFaturamento()
        self.notificador = NotificadorAuditoria()


    def render(self, page, *argumentos):
        # *argumentos junta numa tupla tudo o que vier depois do nome da página
        # (o usuário logado, um id, uma mensagem de erro...) e repassa
        # para o método da página, na mesma ordem.
        content = self.pages.get(page, self.helper)
        return content(*argumentos)


    def helper(self, *argumentos):
        return template('app/views/html/helper')


    def index(self, usuario=None):
        return template('app/views/html/index', usuario=usuario)


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

    def nao_encontrado(self, usuario, mensagem):
        return template('app/views/html/nao_encontrado', usuario=usuario, mensagem=mensagem)


    # ------------------------------------------------------------------
    # Login

    def login_pagina(self, usuario=None, erro=None):
        return template('app/views/html/login', erro=erro)

    def autenticar(self, login, senha):
        # Devolve o usuário se o login e a senha estiverem certos; senão, None
        usuario = self.usuarios.buscar_por_login(login.strip().lower())
        if usuario is None:
            return None
        if not usuario.verificar_senha(senha):
            return None
        return usuario

    def buscar_usuario(self, id):
        return self.usuarios.buscar_por_id(id)

    def acesso_negado(self, usuario):
        return template('app/views/html/acesso_negado', usuario=usuario)


    # ------------------------------------------------------------------
    # Painel (página de acesso restrito)

    def painel(self, usuario):
        total_alertas = 0
        com_alerta = 0
        meus = 0
        ultimos_alertas = []

        for atendimento in reversed(self.atendimentos.listar()):
            sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)
            total_alertas = total_alertas + len(nao_faturados)
            if len(nao_faturados) > 0:
                com_alerta = com_alerta + 1
                if len(ultimos_alertas) < 5:
                    ultimos_alertas.append({
                        'atendimento': atendimento,
                        'nao_faturados': nao_faturados
                    })
            if atendimento.autor == usuario.login:
                meus = meus + 1

        return template('app/views/html/painel',
                        usuario=usuario,
                        total_atendimentos=len(self.atendimentos.listar()),
                        com_alerta=com_alerta,
                        total_alertas=total_alertas,
                        meus=meus,
                        total_procedimentos=len(self.procedimentos.listar()),
                        total_usuarios=len(self.usuarios.listar()),
                        ultimos_alertas=ultimos_alertas)


    # ------------------------------------------------------------------
    # Páginas de atendimentos

    def atendimentos_lista(self, usuario):
        linhas = []
        # reversed: o atendimento mais novo aparece primeiro
        for atendimento in reversed(self.atendimentos.listar()):
            sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)
            linhas.append({
                'atendimento': atendimento,
                'alertas': len(nao_faturados),
                'avisos': len(sem_evidencia)
            })
        return template('app/views/html/atendimentos', usuario=usuario, linhas=linhas)

    def atendimento_novo(self, usuario):
        return template('app/views/html/atendimento_form',
                        usuario=usuario,
                        titulo='Novo atendimento',
                        acao='/atendimentos',
                        atendimento=None,
                        procedimentos=self.procedimentos.listar())

    def atendimento_editar(self, usuario, id):
        atendimento = self.atendimentos.buscar_por_id(id)
        if atendimento is None:
            return self.nao_encontrado(usuario, 'Atendimento não encontrado.')
        return template('app/views/html/atendimento_form',
                        usuario=usuario,
                        titulo='Editar atendimento nº ' + str(id),
                        acao='/atendimentos/' + str(id) + '/editar',
                        atendimento=atendimento,
                        procedimentos=self.procedimentos.listar())

    def atendimento_detalhe(self, usuario, id):
        atendimento = self.atendimentos.buscar_por_id(id)
        if atendimento is None:
            return self.nao_encontrado(usuario, 'Atendimento não encontrado.')

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
                        usuario=usuario,
                        atendimento=atendimento,
                        sugestoes=sugestoes,
                        faturados=faturados,
                        nao_faturados=nao_faturados,
                        sem_evidencia=sem_evidencia_descritos,
                        palavras=palavras)


    # Ações (chamadas pelas rotas POST)

    def criar_atendimento(self, texto, faturados, autor):
        novo_id = self.atendimentos.proximo_id()
        data = datetime.now().strftime('%d/%m/%Y %H:%M')
        atendimento = Atendimento(novo_id, texto, faturados, data, autor.login)
        self.atendimentos.adicionar(atendimento)
        self.avisar_auditoria(atendimento, 'cadastrado', autor)   # Nível 4
        return novo_id

    def editar_atendimento(self, id, texto, faturados, quem):
        antigo = self.atendimentos.buscar_por_id(id)
        if antigo is None:
            return False
        # A data e o autor do cadastro continuam os mesmos
        novo = Atendimento(id, texto, faturados, antigo.data, antigo.autor)
        self.atendimentos.atualizar(novo)
        self.avisar_auditoria(novo, 'editado', quem)              # Nível 4
        return True

    def excluir_atendimento(self, id, quem):
        atendimento = self.atendimentos.buscar_por_id(id)
        if atendimento is None:
            return False
        self.atendimentos.remover(id)
        # Nível 4: avisa o painel para tirar o atendimento da fila
        mensagem = self.montar_mensagem('excluido', atendimento, [], 'excluído', quem.nome)
        self.notificador.enviar(mensagem)
        return True


    # ------------------------------------------------------------------
    # Nível 4: painel de auditoria em tempo real

    def nome_do_autor(self, login):
        # O atendimento guarda só o login; aqui buscamos o nome da pessoa
        usuario = self.usuarios.buscar_por_login(login)
        if usuario is None:
            return login if login != '' else 'desconhecido'
        return usuario.nome

    def montar_mensagem(self, tipo, atendimento, nao_faturados, acao, quem, horario=None):
        """Monta o dicionário que vai para o painel de auditoria.

        tipo: 'alerta' (tem procedimento não faturado), 'ok' (tudo faturado)
              ou 'excluido' (o atendimento foi apagado).
        O mesmo formato serve para os cartões que já aparecem quando a
        página abre e para as mensagens que chegam pelo WebSocket.
        """
        if horario is None:
            horario = datetime.now().strftime('%H:%M:%S')
        procedimentos = []
        for sugestao in nao_faturados:
            procedimentos.append({
                'codigo': sugestao.procedimento.codigo,
                'nome': sugestao.procedimento.nome,
                'porcentagem': sugestao.porcentagem
            })
        return {
            'tipo': tipo,
            'id': atendimento.id,
            'acao': acao,
            'quem': quem,
            'horario': horario,
            'resumo': atendimento.resumo(140),
            'procedimentos': procedimentos
        }

    def avisar_auditoria(self, atendimento, acao, quem):
        # Analisa o atendimento salvo e manda o resultado para os painéis abertos
        sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)
        if len(nao_faturados) > 0:
            tipo = 'alerta'
        else:
            tipo = 'ok'
        mensagem = self.montar_mensagem(tipo, atendimento, nao_faturados, acao, quem.nome)
        self.notificador.enviar(mensagem)

    def auditoria(self, usuario):
        # Quando a página abre, a fila já mostra os atendimentos com alerta.
        # Depois, o WebSocket acrescenta os novos sem recarregar.
        alertas = []
        total_procedimentos = 0
        for atendimento in reversed(self.atendimentos.listar()):
            sugestoes, nao_faturados, sem_evidencia = self.analisar(atendimento)
            if len(nao_faturados) > 0:
                alertas.append(self.montar_mensagem('alerta', atendimento, nao_faturados,
                                                    'cadastrado',
                                                    self.nome_do_autor(atendimento.autor),
                                                    atendimento.data))
                total_procedimentos = total_procedimentos + len(nao_faturados)
        return template('app/views/html/auditoria',
                        usuario=usuario,
                        alertas=alertas,
                        total_procedimentos=total_procedimentos)


    # ------------------------------------------------------------------
    # Páginas do catálogo de procedimentos

    def procedimentos_lista(self, usuario):
        return template('app/views/html/procedimentos',
                        usuario=usuario,
                        procedimentos=self.procedimentos.listar())

    def procedimento_novo(self, usuario, erro=None):
        return template('app/views/html/procedimento_form',
                        usuario=usuario,
                        titulo='Novo procedimento',
                        acao='/procedimentos',
                        procedimento=None,
                        erro=erro)

    def procedimento_editar(self, usuario, codigo):
        procedimento = self.procedimentos.buscar_por_id(codigo)
        if procedimento is None:
            return self.nao_encontrado(usuario, 'Procedimento não encontrado.')
        return template('app/views/html/procedimento_form',
                        usuario=usuario,
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


    # ------------------------------------------------------------------
    # Páginas de usuários (só o administrador chega aqui)

    def usuarios_lista(self, usuario, erro=None):
        return template('app/views/html/usuarios',
                        usuario=usuario,
                        usuarios=self.usuarios.listar(),
                        erro=erro)

    def usuario_novo(self, usuario, erro=None):
        return template('app/views/html/usuario_form',
                        usuario=usuario,
                        titulo='Novo usuário',
                        acao='/usuarios',
                        editado=None,
                        erro=erro)

    def usuario_editar(self, usuario, id, erro=None):
        editado = self.usuarios.buscar_por_id(id)
        if editado is None:
            return self.nao_encontrado(usuario, 'Usuário não encontrado.')
        return template('app/views/html/usuario_form',
                        usuario=usuario,
                        titulo='Editar usuário',
                        acao='/usuarios/' + str(id) + '/editar',
                        editado=editado,
                        erro=erro)


    # Ações (chamadas pelas rotas POST). Devolvem uma mensagem de erro, ou None.

    def conferir_senha(self, senha, confirmar):
        if len(senha) < 6:
            return 'A senha precisa ter pelo menos 6 caracteres.'
        if senha != confirmar:
            return 'As duas senhas não são iguais.'
        return None

    def cadastrar_usuario(self, nome, login, tipo, senha, confirmar):
        nome = nome.strip()
        login = login.strip().lower()
        if nome == '' or login == '':
            return 'Preencha o nome e o login.'
        if ' ' in login:
            return 'O login não pode ter espaços.'
        if tipo != 'codificador' and tipo != 'administrador':
            return 'Escolha um tipo de usuário válido.'
        if self.usuarios.buscar_por_login(login) is not None:
            return 'Já existe um usuário com o login ' + login + '.'
        erro = self.conferir_senha(senha, confirmar)
        if erro is not None:
            return erro
        usuario = novo_usuario(self.usuarios.proximo_id(), nome, login, senha, tipo)
        self.usuarios.adicionar(usuario)
        return None

    def editar_usuario(self, id, nome, tipo, nova_senha, confirmar, usuario_logado):
        antigo = self.usuarios.buscar_por_id(id)
        if antigo is None:
            return 'Usuário não encontrado.'
        nome = nome.strip()
        if nome == '':
            return 'Preencha o nome.'
        if tipo != 'codificador' and tipo != 'administrador':
            return 'Escolha um tipo de usuário válido.'
        # O administrador não pode tirar a própria permissão
        if antigo.id == usuario_logado.id and tipo != antigo.tipo():
            return 'Você não pode mudar o seu próprio tipo.'
        if nova_senha != '':
            erro = self.conferir_senha(nova_senha, confirmar)
            if erro is not None:
                return erro
        self.usuarios.atualizar(antigo.editado(nome, tipo, nova_senha))
        return None

    def excluir_usuario(self, id, usuario_logado):
        if id == usuario_logado.id:
            return 'Você não pode excluir a sua própria conta.'
        if not self.usuarios.remover(id):
            return 'Usuário não encontrado.'
        return None
