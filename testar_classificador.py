# Testa o classificador no terminal, sem servidor.
# Rodar na raiz do projeto: python testar_classificador.py

import json

from app.models.repositorio import RepositorioProcedimentos
from app.models.classificador import ClassificadorPalavrasChave


repositorio = RepositorioProcedimentos()
classificador = ClassificadorPalavrasChave(repositorio.listar())

with open('app/controllers/db/textos_teste.json', 'r', encoding='utf-8') as arquivo:
    textos = json.load(arquivo)

acertos = 0
for numero, caso in enumerate(textos, start=1):
    sugestoes = classificador.sugerir(caso['texto'])

    sugeridos = []
    for sugestao in sugestoes:
        sugeridos.append(sugestao.procedimento.codigo)

    gabarito = caso['gabarito']
    certo = sorted(sugeridos) == sorted(gabarito)
    if certo:
        acertos += 1

    print('Texto', numero, '-', 'OK' if certo else 'DIFERENTE')
    print('  ', caso['texto'])
    for sugestao in sugestoes:
        print('   sugerido:', sugestao.procedimento.nome, '| pontuação', round(sugestao.pontuacao, 2))
    for codigo in gabarito:
        if codigo not in sugeridos:
            print('   faltou:', codigo)
    for codigo in sugeridos:
        if codigo not in gabarito:
            print('   sobrou:', codigo)
    print()

print('Textos com resultado igual ao gabarito:', acertos, 'de', len(textos))
