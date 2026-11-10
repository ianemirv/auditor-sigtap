class Procedimento:
    """Um procedimento da tabela SIGTAP: código, nome e palavras-chave."""

    def __init__(self, codigo, nome, palavras_chave):
        # O "_" no começo avisa: atributo privado, não mexa de fora da classe
        self._codigo = codigo
        self._nome = nome
        self._palavras_chave = palavras_chave

    # @property deixa ler o atributo como se fosse uma variável: p.nome
    @property
    def id(self):
        # No repositório, o código é o que identifica cada procedimento
        return self._codigo

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @property
    def palavras_chave(self):
        return self._palavras_chave

    def to_dict(self):
        # Transforma o objeto num dicionário, para salvar no JSON
        return {
            'codigo': self._codigo,
            'nome': self._nome,
            'palavras_chave': self._palavras_chave
        }

    @staticmethod
    def from_dict(dados):
        # Faz o caminho contrário: dicionário do JSON -> objeto
        return Procedimento(dados['codigo'], dados['nome'], dados['palavras_chave'])
