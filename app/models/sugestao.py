class Sugestao:
    """Um procedimento que o classificador achou no texto, com a pontuação.

    Composição: uma Sugestao CONTÉM um Procedimento.
    """

    def __init__(self, procedimento, pontuacao, palavras_encontradas):
        self._procedimento = procedimento
        self._pontuacao = pontuacao                      # de 0 a 1
        self._palavras_encontradas = palavras_encontradas

    @property
    def procedimento(self):
        return self._procedimento

    @property
    def pontuacao(self):
        return self._pontuacao

    @property
    def palavras_encontradas(self):
        return self._palavras_encontradas

    @property
    def porcentagem(self):
        # 0.4 -> 40, para a barra da página
        return int(round(self._pontuacao * 100))
