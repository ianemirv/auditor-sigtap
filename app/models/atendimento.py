class Atendimento:
    """Um atendimento: texto clínico, códigos faturados, data e quem cadastrou."""

    def __init__(self, id, texto, faturados, data, autor=''):
        self._id = id
        self._texto = texto
        self._faturados = faturados   # lista de códigos SIGTAP
        self._data = data
        self._autor = autor           # login de quem cadastrou

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

    @property
    def autor(self):
        return self._autor

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
            'data': self._data,
            'autor': self._autor
        }

    @staticmethod
    def from_dict(dados):
        # .get: os atendimentos antigos (Nível 2) não têm autor
        return Atendimento(dados['id'], dados['texto'], dados['faturados'],
                           dados['data'], dados.get('autor', ''))
