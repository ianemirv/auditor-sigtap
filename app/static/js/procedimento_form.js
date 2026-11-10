const formulario = document.getElementById('form-procedimento');
const campoCodigo = document.getElementById('codigo');
const campoNome = document.getElementById('nome');
const campoPalavras = document.getElementById('palavras_chave');
const previa = document.getElementById('previa');
const mensagemErro = document.getElementById('erro-procedimento');

// 1. Mostra as palavras-chave como etiquetas enquanto a pessoa digita
function separarPalavras() {
  const palavras = [];
  for (const pedaco of campoPalavras.value.split(',')) {
    const limpo = pedaco.trim();
    if (limpo !== '') {
      palavras.push(limpo);
    }
  }
  return palavras;
}

function atualizarPrevia() {
  previa.innerHTML = '';
  for (const palavra of separarPalavras()) {
    const etiqueta = document.createElement('span');
    etiqueta.className = 'etiqueta';
    etiqueta.textContent = palavra;
    previa.appendChild(etiqueta);
  }
}

campoPalavras.addEventListener('input', atualizarPrevia);
atualizarPrevia();

// 2. Não deixa enviar com campo vazio
formulario.addEventListener('submit', function (evento) {
  const codigoVazio = campoCodigo.value.trim() === '';
  const nomeVazio = campoNome.value.trim() === '';
  const semPalavras = separarPalavras().length === 0;
  if (codigoVazio || nomeVazio || semPalavras) {
    evento.preventDefault();
    mensagemErro.style.display = 'block';
  }
});
