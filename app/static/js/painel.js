// 1. Saudação de acordo com a hora do computador
const saudacao = document.getElementById('saudacao');
const nome = saudacao.dataset.nome;   // vem do atributo data-nome do HTML
const hora = new Date().getHours();

if (hora < 12) {
  saudacao.textContent = 'Bom dia, ' + nome;
} else if (hora < 18) {
  saudacao.textContent = 'Boa tarde, ' + nome;
} else {
  saudacao.textContent = 'Boa noite, ' + nome;
}

// 2. Os números dos cartões sobem de 0 até o valor certo
const numeros = document.querySelectorAll('.numero');

for (const elemento of numeros) {
  const final = Number(elemento.dataset.numero);
  let atual = 0;
  elemento.textContent = '0';

  if (final > 0) {
    const relogio = setInterval(function () {
      atual = atual + 1;
      elemento.textContent = atual;
      if (atual >= final) {
        clearInterval(relogio);   // chegou no valor: para de contar
      }
    }, 600 / final);              // quanto maior o número, mais rápido sobe
  }
}
