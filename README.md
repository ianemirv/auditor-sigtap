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

## Nível 2

CRUD completo de **atendimentos** (texto clínico + procedimentos faturados) e do
**catálogo SIGTAP** (16 procedimentos de laboratório, imagem e ECG).
Ao abrir um atendimento, o sistema:

1. sugere os procedimentos SIGTAP citados no texto, com uma pontuação de confiança;
2. mostra em vermelho o que está no texto e **não foi faturado** (possível subfaturamento);
3. mostra em amarelo o que foi faturado **sem evidência** no texto.

| Rota | Método | O que faz |
| --- | --- | --- |
| `/atendimentos` | GET | Lista os atendimentos e quantos alertas cada um tem |
| `/atendimentos/novo` | GET | Formulário de cadastro |
| `/atendimentos` | POST | Cria o atendimento |
| `/atendimentos/<id>` | GET | Detalhe com sugestões e alertas |
| `/atendimentos/<id>/editar` | GET/POST | Edita |
| `/atendimentos/<id>/excluir` | POST | Exclui |
| `/procedimentos` (+ `/novo`, `/<codigo>/editar`, `/<codigo>/excluir`) | GET/POST | CRUD do catálogo |

### Classes (em `app/models/`)

| Classe | Papel | Conceito de OO |
| --- | --- | --- |
| `Procedimento`, `Atendimento` | Os dados | Encapsulamento (`@property`) |
| `RepositorioJSON` | Carregar, salvar, listar, buscar, adicionar, atualizar e remover em JSON | Classe base |
| `RepositorioProcedimentos`, `RepositorioAtendimentos` | Um repositório para cada modelo | Herança |
| `Sugestao` | Procedimento sugerido + pontuação | Composição |
| `Classificador` | Define `sugerir(texto)` | Classe abstrata (`abc`) |
| `ClassificadorPalavrasChave` | Pontuação = palavras-chave achadas ÷ total; sugere a partir de 0,3 | Herança + polimorfismo |
| `AnalisadorFaturamento` | Compara sugestões com o faturado | Responsabilidade única |

Os dados ficam em `app/controllers/db/` (`procedimentos.json`, `atendimentos.json`, `textos_teste.json`).

### JavaScript do nível

- Confirmação antes de excluir (`confirmar_exclusao.js`)
- Contador de caracteres, contador de faturados marcados e bloqueio de texto vazio (`atendimento_form.js`)
- Destaque, no texto clínico, das palavras-chave encontradas (`atendimento_detalhe.js`)
- Prévia das palavras-chave como etiquetas e validação (`procedimento_form.js`)

### Testando o classificador no terminal

`python testar_classificador.py` roda o classificador nos 16 textos de teste e compara com o gabarito.
Resultado atual: 13 de 16 iguais ao gabarito. Os 3 erros são casos difíceis de propósito:
exame citado mas recusado pelo paciente (negação), "PCR" no sentido de parada cardiorrespiratória
(ambiguidade) e "ultrasonografia" escrita errado.

## Como rodar

1. Instalar o Bottle: `pip install bottle`
2. Executar o arquivo `route.py`, na raiz do projeto: `python route.py`
3. Abrir http://localhost:8080 no navegador.

## Trabalhando com o BMVC no DOCKER

1. `docker build -t bmvci .`
2. `docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci`
