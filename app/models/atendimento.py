class Atendimento:
    """Um atendimento: texto clínico, códigos faturados e data."""

    def __init__(self, id, texto, faturados, data):
        self._id = id
        self._texto = texto
        self._faturados = faturados   # lista de códigos SIGTAP
        self._data = data

    @property
    def id(self):
        return self._id

    @property
    def texto(self):
        return self._texto

    @property
    def faturados(self):
        return self._faturados

    @property
    def data(self):
        return self._data

    def resumo(self, tamanho=80):
        # Começo do texto, para mostrar na tabela da lista
        if len(self._texto) <= tamanho:
            return self._texto
        return self._texto[:tamanho] + '...'

    def to_dict(self):
        return {
            'id': self._id,
            'texto': self._texto,
            'faturados': self._faturados,
            'data': self._data
        }

    @staticmethod
    def from_dict(dados):
        return Atendimento(dados['id'], dados['texto'], dados['faturados'], dados['data'])
