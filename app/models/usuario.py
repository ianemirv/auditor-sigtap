import hashlib
import secrets
from abc import ABC, abstractmethod


class Usuario(ABC):
    """Pessoa que usa o sistema.

    A senha NUNCA é guardada. Guardamos só o hash dela (a senha embaralhada)
    e o sal (um texto aleatório, diferente para cada usuário).
    """

    def __init__(self, id, nome, login, senha_hash, sal):
        self._id = id
        self._nome = nome
        self._login = login
        self._senha_hash = senha_hash
        self._sal = sal

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def login(self):
        return self._login

    # ------------------------------------------------------------------
    # Senha

    @staticmethod
    def gerar_hash(senha, sal):
        # pbkdf2 aplica o sha256 100 mil vezes seguidas.
        # Para o usuário isso é instantâneo, mas para quem tenta adivinhar
        # milhões de senhas fica muito lento.
        resultado = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'),
                                        sal.encode('utf-8'), 100000)
        return resultado.hex()

    def verificar_senha(self, senha):
        # Embaralha a senha digitada do mesmo jeito e compara com a guardada
        tentativa = Usuario.gerar_hash(senha, self._sal)
        return secrets.compare_digest(tentativa, self._senha_hash)

    def editado(self, nome, tipo, nova_senha):
        """Devolve um novo usuário com os dados trocados. O login não muda.

        Se a nova senha vier vazia, continua a senha antiga.
        O tipo pode mudar, por isso é criado um objeto novo (de outra classe).
        """
        if nova_senha == '':
            return montar_usuario(tipo, self._id, nome, self._login,
                                  self._senha_hash, self._sal)
        return novo_usuario(self._id, nome, self._login, nova_senha, tipo)

    # ------------------------------------------------------------------
    # Tipo e permissões (as classes filhas mudam o que precisam)

    @abstractmethod
    def tipo(self):
        pass

    def pode_editar_catalogo(self):
        return False

    def pode_gerenciar_usuarios(self):
        return False

    def pode_ver_auditoria(self):
        return False

    # ------------------------------------------------------------------
    # JSON

    def to_dict(self):
        return {
            'id': self._id,
            'nome': self._nome,
            'login': self._login,
            'tipo': self.tipo(),
            'senha_hash': self._senha_hash,
            'sal': self._sal
        }

    @staticmethod
    def from_dict(dados):
        return montar_usuario(dados['tipo'], dados['id'], dados['nome'],
                              dados['login'], dados['senha_hash'], dados['sal'])


class Codificador(Usuario):
    """Cadastra e confere atendimentos. Só olha o catálogo, não edita."""

    def tipo(self):
        return 'codificador'


class Administrador(Usuario):
    """Faz tudo: edita o catálogo SIGTAP, cuida dos usuários e vê a auditoria."""

    def tipo(self):
        return 'administrador'

    # Sobrescreve os métodos da classe mãe (polimorfismo)
    def pode_editar_catalogo(self):
        return True

    def pode_gerenciar_usuarios(self):
        return True

    def pode_ver_auditoria(self):
        return True


# ----------------------------------------------------------------------
# Funções para criar o objeto da classe certa


def montar_usuario(tipo, id, nome, login, senha_hash, sal):
    if tipo == 'administrador':
        return Administrador(id, nome, login, senha_hash, sal)
    return Codificador(id, nome, login, senha_hash, sal)


def novo_usuario(id, nome, login, senha, tipo):
    """Cria um usuário a partir da senha digitada, já protegida com hash."""
    sal = secrets.token_hex(16)
    senha_hash = Usuario.gerar_hash(senha, sal)
    return montar_usuario(tipo, id, nome, login, senha_hash, sal)
