const formulario = document.getElementById('form-usuario');
const campoNome = document.getElementById('nome');
const campoLogin = document.getElementById('login');
const campoSenha = document.getElementById('senha');
const campoConfirmar = document.getElementById('confirmar');
const botaoMostrar = document.getElementById('botao-mostrar');
const situacao = document.getElementById('situacao-senha');
const mensagemErro = document.getElementById('erro-usuario');

// No cadastro a senha é obrigatória; na edição pode ficar vazia
const senhaObrigatoria = formulario.dataset.senhaObrigatoria === 'sim';

// 1. Mostrar ou esconder as duas senhas
botaoMostrar.addEventListener('click', function () {
  if (campoSenha.type === 'password') {
    campoSenha.type = 'text';
    campoConfirmar.type = 'text';
    botaoMostrar.textContent = 'Ocultar';
  } else {
    campoSenha.type = 'password';
    campoConfirmar.type = 'password';
    botaoMostrar.textContent = 'Mostrar';
  }
});

// 2. Enquanto digita, avisa se a senha é curta ou se as duas são diferentes
function atualizarSituacao() {
  const senha = campoSenha.value;
  if (senha === '') {
    situacao.textContent = '';
  } else if (senha.length < 6) {
    situacao.textContent = 'Senha curta: use pelo menos 6 caracteres.';
  } else if (campoConfirmar.value !== senha) {
    situacao.textContent = 'As senhas ainda não são iguais.';
  } else {
    situacao.textContent = 'Senhas iguais ✓';
  }
}

campoSenha.addEventListener('input', atualizarSituacao);
campoConfirmar.addEventListener('input', atualizarSituacao);

// 3. Confere tudo antes de enviar
function encontrarErro() {
  if (campoNome.value.trim() === '' || campoLogin.value.trim() === '') {
    return 'Preencha o nome e o login.';
  }
  if (campoLogin.value.trim().includes(' ')) {
    return 'O login não pode ter espaços.';
  }
  const senha = campoSenha.value;
  if (senha === '' && !senhaObrigatoria) {
    return '';   // edição sem trocar a senha
  }
  if (senha.length < 6) {
    return 'A senha precisa ter pelo menos 6 caracteres.';
  }
  if (senha !== campoConfirmar.value) {
    return 'As duas senhas não são iguais.';
  }
  return '';
}

formulario.addEventListener('submit', function (evento) {
  const erro = encontrarErro();
  if (erro !== '') {
    evento.preventDefault();
    mensagemErro.textContent = erro;
    mensagemErro.style.display = 'block';
  }
});
