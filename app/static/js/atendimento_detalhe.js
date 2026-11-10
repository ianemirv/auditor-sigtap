// Destaca no texto clínico as palavras-chave que o classificador encontrou.
// As palavras chegam do servidor no atributo data-palavras, separadas por "|".

const paragrafo = document.getElementById('texto-clinico');
const botaoDestacar = document.getElementById('botao-destacar');

const textoOriginal = paragrafo.textContent;
const palavras = paragrafo.dataset.palavras.split('|');
let destacado = false;

// Deixa uma letra igual ao que o Python faz: minúscula e sem acento.
// Se não for letra nem número, vira espaço.
function normalizarLetra(letra) {
  const semAcento = letra.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  if (semAcento.length === 1 && /[a-z0-9]/.test(semAcento)) {
    return semAcento;
  }
  return ' ';
}

// Troca < > & por códigos, para o texto não virar HTML sem querer
function protegerHTML(letra) {
  if (letra === '<') return '&lt;';
  if (letra === '>') return '&gt;';
  if (letra === '&') return '&amp;';
  return letra;
}

function textoComDestaque() {
  // 1. Cópia normalizada do texto, letra por letra (mesmo tamanho do original)
  let normal = '';
  for (let i = 0; i < textoOriginal.length; i++) {
    normal += normalizarLetra(textoOriginal[i]);
  }

  // 2. Marca quais posições fazem parte de uma palavra-chave
  const marcar = [];
  for (let i = 0; i < textoOriginal.length; i++) {
    marcar.push(false);
  }

  const comEspacos = ' ' + normal + ' ';
  for (const palavra of palavras) {
    if (palavra === '') continue;
    let posicao = comEspacos.indexOf(' ' + palavra + ' ');
    while (posicao !== -1) {
      for (let i = posicao; i < posicao + palavra.length; i++) {
        marcar[i] = true;
      }
      posicao = comEspacos.indexOf(' ' + palavra + ' ', posicao + 1);
    }
  }

  // 3. Monta o HTML com <mark> em volta dos trechos marcados
  let html = '';
  for (let i = 0; i < textoOriginal.length; i++) {
    const comecaMarca = marcar[i] && (i === 0 || !marcar[i - 1]);
    const terminaMarca = marcar[i] && (i === textoOriginal.length - 1 || !marcar[i + 1]);
    if (comecaMarca) html += '<mark>';
    html += protegerHTML(textoOriginal[i]);
    if (terminaMarca) html += '</mark>';
  }
  return html;
}

botaoDestacar.addEventListener('click', function () {
  if (destacado) {
    paragrafo.textContent = textoOriginal;
    botaoDestacar.textContent = 'Destacar palavras-chave';
  } else {
    paragrafo.innerHTML = textoComDestaque();
    botaoDestacar.textContent = 'Tirar destaque';
  }
  destacado = !destacado;
});

// Sem palavras encontradas, não há o que destacar
if (palavras.length === 1 && palavras[0] === '') {
  botaoDestacar.disabled = true;
  botaoDestacar.textContent = 'Nada para destacar';
}
