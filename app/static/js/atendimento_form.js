const formulario = document.getElementById('form-atendimento');
const campoTexto = document.getElementById('texto');
const contador = document.getElementById('contador');
const mensagemErro = document.getElementById('erro-texto');
const caixas = document.querySelectorAll('input[name="faturados"]');
const totalMarcados = document.getElementById('total-marcados');

// 1. Contador de caracteres do texto clínico
function atualizarContador() {
  contador.textContent = campoTexto.value.length + ' caracteres';
}

campoTexto.addEventListener('input', function () {
  atualizarContador();
  mensagemErro.style.display = 'none';   // some o erro quando a pessoa digita
});

// 2. Quantos procedimentos estão marcados como faturados
function atualizarMarcados() {
  let total = 0;
  for (const caixa of caixas) {
    if (caixa.checked) {
      total = total + 1;
    }
  }
  totalMarcados.textContent = '(' + total + ' marcado(s))';
}

for (const caixa of caixas) {
  caixa.addEventListener('change', atualizarMarcados);
}

// 3. Não deixa enviar com o texto vazio
formulario.addEventListener('submit', function (evento) {
  if (campoTexto.value.trim() === '') {
    evento.preventDefault();
    mensagemErro.style.display = 'inline';
    campoTexto.focus();
  }
});

// Mostra os números certos assim que a página abre
atualizarContador();
atualizarMarcados();
