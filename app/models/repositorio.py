import json
import os

from app.models.procedimento import Procedimento
from app.models.atendimento import Atendimento


class RepositorioJSON:
    """Guarda uma lista de objetos num arquivo JSON.

    Serve de base: as classes filhas só dizem qual é o arquivo
    e como transformar um dicionário em objeto (criar_objeto).
    """

    def __init__(self, arquivo):
        self._arquivo = arquivo
        self._objetos = []
        self.carregar()

    def criar_objeto(self, dados):
        # Cada classe filha escreve a sua versão deste método
        raise NotImplementedError('A classe filha precisa criar este método')

    def carregar(self):
        self._objetos = []
        if not os.path.exists(self._arquivo):
            return
        with open(self._arquivo, 'r', encoding='utf-8') as arquivo:
            lista_de_dicionarios = json.load(arquivo)
        for dados in lista_de_dicionarios:
            self._objetos.append(self.criar_objeto(dados))

    def salvar(self):
        lista_de_dicionarios = []
        for objeto in self._objetos:
            lista_de_dicionarios.append(objeto.to_dict())
        with open(self._arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_de_dicionarios, arquivo, ensure_ascii=False, indent=2)

    def listar(self):
        # Devolve uma cópia, para ninguém alterar a lista de fora da classe
        return list(self._objetos)

    def buscar_por_id(self, id):
        for objeto in self._objetos:
            if objeto.id == id:
                return objeto
        return None

    def adicionar(self, objeto):
        self._objetos.append(objeto)
        self.salvar()

    def atualizar(self, objeto_novo):
        for i in range(len(self._objetos)):
            if self._objetos[i].id == objeto_novo.id:
                self._objetos[i] = objeto_novo
                self.salvar()
                return True
        return False

    def remover(self, id):
        objeto = self.buscar_por_id(id)
        if objeto is None:
            return False
        self._objetos.remove(objeto)
        self.salvar()
        return True


class RepositorioProcedimentos(RepositorioJSON):

    def __init__(self):
        super().__init__('app/controllers/db/procedimentos.json')

    def criar_objeto(self, dados):
        return Procedimento.from_dict(dados)


class RepositorioAtendimentos(RepositorioJSON):

    def __init__(self):
        super().__init__('app/controllers/db/atendimentos.json')

    def criar_objeto(self, dados):
        return Atendimento.from_dict(dados)

    def proximo_id(self):
        # O maior id que existe + 1
        maior = 0
        for atendimento in self._objetos:
            if atendimento.id > maior:
                maior = atendimento.id
        return maior + 1
