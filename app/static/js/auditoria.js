// Painel de auditoria: recebe as mensagens do servidor por WebSocket
// e atualiza a página sozinho, sem recarregar.

const estado = document.getElementById('estado-conexao');
const textoEstado = document.getElementById('texto-estado');
const fila = document.getElementById('fila');
const filaVazia = document.getElementById('fila-vazia');
const atividade = document.getElementById('atividade');
const atividadeVazia = document.getElementById('atividade-vazia');
const contadorFila = document.getElementById('contador-fila');
const contadorProcedimentos = document.getElementById('contador-procedimentos');
const contadorAoVivo = document.getElementById('contador-ao-vivo');

let recebidosAoVivo = 0;
let podeReconectar = true;


// ---------- 1. A conexão ----------

function mostrarEstado(nome, texto) {
  // nome: 'conectando', 'conectado' ou 'desconectado' (cada um tem uma cor no CSS)
  estado.className = 'estado estado-' + nome;
  textoEstado.textContent = texto;
}

function conectar() {
  mostrarEstado('conectando', 'Conectando...');

  // location.host é "localhost:8080": o mesmo servidor que mandou a página
  const conexao = new WebSocket('ws://' + location.host + '/ws/auditoria');

  conexao.onopen = function () {
    mostrarEstado('conectado', 'Conectado: recebendo ao vivo');
  };

  // Roda toda vez que o servidor manda uma mensagem
  conexao.onmessage = function (evento) {
    const dados = JSON.parse(evento.data);   // texto JSON -> objeto
    receber(dados);
  };

  // Roda quando a conexão cai (servidor desligado, internet, etc.)
  conexao.onclose = function () {
    if (!podeReconectar) {
      return;
    }
    mostrarEstado('desconectado', 'Sem conexão. Tentando de novo em 3 s...');
    setTimeout(conectar, 3000);   // reconexão automática
  };
}


// ---------- 2. O que fazer com cada mensagem ----------

function receber(dados) {
  if (dados.tipo === 'negado') {
    // O servidor recusou: login vencido ou usuário sem permissão
    podeReconectar = false;
    mostrarEstado('desconectado', 'Sessão encerrada. Entre de novo no sistema.');
    return;
  }

  if (dados.tipo === 'alerta') {
    tirarDaFila(dados.id, false);   // se o atendimento já estava na fila, sai o cartão antigo
    fila.prepend(criarCartao(dados));   // prepend: coloca no topo da lista
    recebidosAoVivo = recebidosAoVivo + 1;
  } else {
    // 'ok' (tudo faturado) ou 'excluido': o atendimento sai da fila
    tirarDaFila(dados.id, true);
  }

  registrarAtividade(dados);
  atualizarContadores();
}


// ---------- 3. Cartões da fila ----------

function criarElemento(tag, classe, texto) {
  const elemento = document.createElement(tag);
  elemento.className = classe;
  // textContent: o texto aparece como texto, nunca vira HTML
  elemento.textContent = texto;
  return elemento;
}

function criarCartao(dados) {
  const cartao = criarElemento('article', 'cartao-auditoria chegando', '');
  cartao.dataset.id = dados.id;
  cartao.dataset.procedimentos = dados.procedimentos.length;

  const topo = criarElemento('div', 'cartao-topo', '');
  topo.appendChild(criarElemento('strong', '', 'Atendimento nº ' + dados.id));
  topo.appendChild(criarElemento('span', 'selo selo-novo', 'novo · ' + dados.acao));
  cartao.appendChild(topo);

  cartao.appendChild(criarElemento('p', 'cartao-quem', 'por ' + dados.quem + ' · ' + dados.horario));
  cartao.appendChild(criarElemento('p', 'cartao-resumo', dados.resumo));
  cartao.appendChild(criarElemento('p', 'cartao-legenda', 'Citado no texto e não faturado:'));

  const selos = criarElemento('div', 'cartao-selos', '');
  for (const procedimento of dados.procedimentos) {
    const selo = criarElemento('span', 'selo selo-alerta', procedimento.nome);
    selo.title = procedimento.codigo + ' · ' + procedimento.porcentagem + '% de confiança';
    selos.appendChild(selo);
  }
  cartao.appendChild(selos);

  const link = criarElemento('a', 'cartao-link', 'Abrir atendimento →');
  link.href = '/atendimentos/' + dados.id;
  cartao.appendChild(link);

  return cartao;
}

function tirarDaFila(id, comAnimacao) {
  const cartao = fila.querySelector('.cartao-auditoria[data-id="' + id + '"]:not(.saindo)');
  if (cartao === null) {
    return;   // não estava na fila
  }
  if (comAnimacao) {
    cartao.classList.add('saindo');   // o CSS faz o cartão sumir aos poucos
    setTimeout(function () {
      cartao.remove();
    }, 400);
  } else {
    cartao.remove();
  }
}


// ---------- 4. Lista de atividade ----------

function registrarAtividade(dados) {
  let texto = 'Nº ' + dados.id + ' ' + dados.acao + ' por ' + dados.quem;

  if (dados.tipo === 'alerta') {
    const quantos = dados.procedimentos.length;
    texto = texto + ': ' + quantos + (quantos === 1 ? ' procedimento não faturado' : ' procedimentos não faturados');
  } else if (dados.tipo === 'ok') {
    texto = texto + ': tudo faturado';
  }

  const item = criarElemento('li', 'atividade-' + dados.tipo, '');
  item.appendChild(criarElemento('span', 'hora', dados.horario));
  item.appendChild(document.createTextNode(texto));
  atividade.prepend(item);

  atividadeVazia.classList.add('escondido');

  // Guarda só as 15 mais recentes
  while (atividade.children.length > 15) {
    atividade.lastElementChild.remove();
  }
}


// ---------- 5. Contadores ----------

function atualizarContadores() {
  // Conta só os cartões que não estão sumindo
  const cartoes = fila.querySelectorAll('.cartao-auditoria:not(.saindo)');
  let procedimentos = 0;
  for (const cartao of cartoes) {
    procedimentos = procedimentos + Number(cartao.dataset.procedimentos);
  }

  contadorFila.textContent = cartoes.length;
  contadorProcedimentos.textContent = procedimentos;
  contadorAoVivo.textContent = recebidosAoVivo;

  if (cartoes.length > 0) {
    filaVazia.classList.add('escondido');
  } else {
    filaVazia.classList.remove('escondido');
  }

  // Mostra o número também na aba do navegador
  document.title = '(' + cartoes.length + ') Auditoria ao vivo — Auditor SIGTAP';
}


conectar();
atualizarContadores();
