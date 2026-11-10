import unicodedata
from abc import ABC, abstractmethod

from app.models.sugestao import Sugestao


class Classificador(ABC):
    """Classe abstrata: diz QUE todo classificador tem sugerir(texto),
    mas não diz COMO. Cada classe filha decide o seu jeito."""

    @abstractmethod
    def sugerir(self, texto):
        pass


def pegar_pontuacao(sugestao):
    # Usada para ordenar a lista de sugestões pela pontuação
    return sugestao.pontuacao


class ClassificadorPalavrasChave(Classificador):
    """Sugere procedimentos contando as palavras-chave que aparecem no texto."""

    def __init__(self, procedimentos, limite=0.3):
        self._procedimentos = procedimentos
        self._limite = limite

    def normalizar(self, texto):
        # 1. tudo minúsculo
        texto = texto.lower()
        # 2. separa a letra do acento ("ó" vira "o" + acento)
        texto = unicodedata.normalize('NFD', texto)
        # 3. guarda só letras e números; o resto (acentos somem, pontuação vira espaço)
        limpo = ''
        for letra in texto:
            if unicodedata.category(letra) == 'Mn':
                continue
            if letra.isalnum():
                limpo += letra
            else:
                limpo += ' '
        # 4. junta as palavras com um espaço só entre elas
        return ' '.join(limpo.split())

    def contem(self, texto_normal, palavra_normal):
        # Os espaços nas pontas fazem achar só palavras inteiras:
        # "eas" não pode ser achada dentro de "areas"
        return (' ' + palavra_normal + ' ') in (' ' + texto_normal + ' ')

    def sugerir(self, texto):
        texto_normal = self.normalizar(texto)
        sugestoes = []

        for procedimento in self._procedimentos:
            encontradas = []
            for palavra in procedimento.palavras_chave:
                palavra_normal = self.normalizar(palavra)
                if self.contem(texto_normal, palavra_normal):
                    encontradas.append(palavra_normal)

            if len(procedimento.palavras_chave) == 0:
                continue
            pontuacao = len(encontradas) / len(procedimento.palavras_chave)

            if pontuacao >= self._limite:
                sugestoes.append(Sugestao(procedimento, pontuacao, encontradas))

        # Da maior pontuação para a menor
        sugestoes.sort(key=pegar_pontuacao, reverse=True)
        return sugestoes
