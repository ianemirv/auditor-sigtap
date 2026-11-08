// Pega os elementos da página pelo id
const botaoExemplo = document.getElementById('botao-exemplo');
const exemplo = document.getElementById('exemplo');
const botaoAnalisar = document.getElementById('botao-analisar');
const resultado = document.getElementById('resultado');

// Clique em "Ver exemplo": mostra o texto clínico
botaoExemplo.addEventListener('click', function () {
  exemplo.style.display = 'block';
  botaoExemplo.style.display = 'none';
});

// Clique em "Analisar": mostra o resultado
botaoAnalisar.addEventListener('click', function () {
  resultado.style.display = 'block';
  botaoAnalisar.textContent = 'Analisado';
});
