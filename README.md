# Auditor SIGTAP

Sistema web em Python (Bottle, padrão BMVC) que lê textos clínicos e avisa
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

## Nível 3

Login, senhas protegidas e permissões. Só quem entrou no sistema usa as páginas internas,
e cada tipo de usuário pode fazer coisas diferentes.

| Usuário de teste | Senha | Tipo | O que pode fazer |
| --- | --- | --- | --- |
| `admin` | `admin123` | Administrador | Tudo: atendimentos, catálogo SIGTAP e usuários |
| `marina` | `marina123` | Codificador | Atendimentos; só consulta o catálogo |

- Sem login, qualquer página interna manda para `/login`.
- Login errado mostra uma mensagem; login certo leva ao `/painel` (página de acesso restrito).
- O codificador que tenta abrir uma página do administrador recebe a página **Acesso negado** (erro 403).
- As senhas **não** são guardadas: `usuarios.json` tem só o hash (PBKDF2 com SHA-256) e um sal aleatório por usuário.
- O cookie de login é **assinado** pelo Bottle: se alguém mudar o valor na mão, ele é ignorado.
- Cada atendimento guarda quem cadastrou.

| Rota | Método | Quem acessa | O que faz |
| --- | --- | --- | --- |
| `/login` | GET/POST | Todos | Formulário e conferência do login |
| `/logout` | GET | Logado | Apaga o cookie e volta para o login |
| `/painel` | GET | Logado | Boas-vindas, números do sistema, últimos alertas e permissões |
| `/atendimentos...` | GET/POST | Logado | CRUD de atendimentos (Nível 2) |
| `/procedimentos` | GET | Logado | Consulta do catálogo |
| `/procedimentos/novo`, `/editar`, `/excluir` | GET/POST | Administrador | CRUD do catálogo |
| `/usuarios` (+ `/novo`, `/<id>/editar`, `/<id>/excluir`) | GET/POST | Administrador | CRUD de usuários |

### Classes novas

| Classe | Papel | Conceito de OO |
| --- | --- | --- |
| `Usuario` | Nome, login, hash e sal da senha; `verificar_senha()`; permissões que devolvem `False` | Classe abstrata + encapsulamento |
| `Codificador(Usuario)` | Usa as permissões da mãe | Herança |
| `Administrador(Usuario)` | Sobrescreve `pode_editar_catalogo()` e `pode_gerenciar_usuarios()` para `True` | Polimorfismo |
| `RepositorioUsuarios` | Guarda os usuários em `usuarios.json`; `buscar_por_login()` | Herança de `RepositorioJSON` |

As rotas só perguntam `usuario.pode_editar_catalogo()`, sem saber se o objeto é
`Codificador` ou `Administrador`.

### JavaScript do nível

- Mostrar/ocultar senha, aviso de campo vazio e aviso de Caps Lock (`login.js`)
- Saudação pela hora do dia e números do painel subindo de 0 até o valor (`painel.js`)
- Mostrar/ocultar senha, aviso de senha curta ou diferente e validação (`usuario_form.js`)

## Nível 4

Painel de **auditoria em tempo real** com WebSocket. O administrador deixa a página
`/auditoria` aberta e, quando qualquer usuário salva um atendimento, o resultado da
análise chega na hora, sem recarregar a página.

- **HTTP normal**: o navegador pergunta e o servidor responde; o servidor nunca fala primeiro.
- **WebSocket**: o navegador abre uma conexão que fica aberta, e o servidor manda mensagens quando quiser.

O que acontece quando um atendimento é salvo:

1. A rota POST chama o controller (`criar_atendimento`, `editar_atendimento` ou `excluir_atendimento`).
2. O controller analisa o atendimento com o `AnalisadorFaturamento` e monta uma mensagem:
   `alerta` (há procedimento citado e não faturado), `ok` (tudo faturado) ou `excluido`.
3. O `NotificadorAuditoria` transforma a mensagem em JSON e manda para todos os painéis abertos.
4. No navegador, o `auditoria.js` recebe a mensagem e atualiza a página:
   - `alerta`: um cartão entra no topo da fila, com animação;
   - `ok` ou `excluido`: o cartão daquele atendimento sai da fila;
   - toda mensagem vira uma linha na lista "Atividade ao vivo", e os contadores se atualizam.

| Rota | Método | Quem acessa | O que faz |
| --- | --- | --- | --- |
| `/auditoria` | GET | Administrador | Página com a fila de auditoria, os contadores e a atividade ao vivo |
| `/ws/auditoria` | WebSocket | Administrador | Conexão que fica aberta para receber as mensagens |

- O WebSocket confere o cookie de login: se não for um administrador, o servidor
  responde `negado` e fecha a conexão.
- O codificador não vê o link "Auditoria ao vivo" e recebe **Acesso negado** (403) se digitar o endereço.
- O servidor padrão do Bottle não aceita WebSocket, então o `route.py` roda com o servidor do
  **gevent** (`server='gevent'`, `handler_class=WebSocketHandler`, da biblioteca `gevent-websocket`).

### Classe nova

| Classe | Papel | Conceito de OO |
| --- | --- | --- |
| `NotificadorAuditoria` | Guarda a lista de conexões abertas (privada); `conectar()`, `desconectar()`, `enviar()` para todas e tira as que caíram | Encapsulamento |

`Usuario` ganhou `pode_ver_auditoria()`, que devolve `False`; `Administrador` sobrescreve para `True`
(o mesmo polimorfismo do Nível 3).

### JavaScript do nível (`auditoria.js`)

- `new WebSocket('ws://' + location.host + '/ws/auditoria')` e `onmessage` para cada mensagem
- Cartões criados na hora, com animação de entrada e de saída
- Indicador de conexão: amarelo (conectando), verde (conectado), vermelho (caiu)
- Reconexão automática 3 segundos depois de a conexão cair
- Contadores e título da aba atualizados a cada mensagem

### Como testar

1. Janela normal: entre como `admin` e abra **Auditoria ao vivo**.
2. Janela anônima ao lado: entre como `marina` e cadastre um atendimento deixando
   de marcar um procedimento citado no texto.
3. O alerta aparece na hora na janela do administrador.
4. Edite o atendimento marcando o que faltava: o cartão sai da fila.

## Como rodar

1. Instalar as bibliotecas: `python -m pip install -r requirements.txt`
   (Bottle, gevent e gevent-websocket)
2. (Opcional) Criar os usuários de teste: `python criar_usuarios.py`.
   O repositório já vem com eles em `app/controllers/db/usuarios.json`.
3. Executar o arquivo `route.py`, na raiz do projeto: `python route.py`
4. Abrir http://localhost:8080 no navegador e clicar em "Entrar no sistema".

## Trabalhando com o BMVC no DOCKER

1. `docker build -t bmvci .`
2. `docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci`
