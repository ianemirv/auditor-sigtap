# Auditor SIGTAP

Sistema web em Python (Bottle, padrão BMVC) que vai ler textos clínicos e avisar
quando um procedimento do SUS foi feito, mas não foi cobrado (subfaturamento).

Projeto da disciplina de Orientação a Objetos da UnB, feito a partir da estrutura
BMVC fornecida na disciplina. Os textos usados são fictícios.

## Nível 1

Página de apresentação (`/`) com CSS e JavaScript próprios
(`app/static/css/index.css` e `app/static/js/index.js`).
O botão "Ver exemplo" mostra um texto clínico, e o botão "Analisar" mostra o resultado
(neste nível o resultado é fixo).

## Como rodar

1. Instalar o Bottle: `pip install bottle`
2. Executar o arquivo `route.py`, na raiz do projeto: `python route.py`
3. Abrir http://localhost:8080 no navegador.

## Trabalhando com o BMVC no DOCKER

1. `docker build -t bmvci .`
2. `docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci`
