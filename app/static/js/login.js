const formulario = document.getElementById('form-login');
const campoLogin = document.getElementById('login');
const campoSenha = document.getElementById('senha');
const botaoMostrar = document.getElementById('botao-mostrar');
const erroLogin = document.getElementById('erro-login');
const erroSenha = document.getElementById('erro-senha');
const avisoCaps = document.getElementById('aviso-caps');

// 1. Botão para mostrar ou esconder a senha
botaoMostrar.addEventListener('click', function () {
  if (campoSenha.type === 'password') {
    campoSenha.type = 'text';
    botaoMostrar.textContent = 'Ocultar';
  } else {
    campoSenha.type = 'password';
    botaoMostrar.textContent = 'Mostrar';
  }
});

// 2. Aviso se algum campo estiver vazio (não envia o formulário)
function marcarCampo(campo, mensagem, vazio) {
  if (vazio) {
    campo.classList.add('campo-errado');
    mensagem.style.display = 'block';
  } else {
    campo.classList.remove('campo-errado');
    mensagem.style.display = 'none';
  }
}

formulario.addEventListener('submit', function (evento) {
  const loginVazio = campoLogin.value.trim() === '';
  const senhaVazia = campoSenha.value === '';
  marcarCampo(campoLogin, erroLogin, loginVazio);
  marcarCampo(campoSenha, erroSenha, senhaVazia);
  if (loginVazio || senhaVazia) {
    evento.preventDefault();
  }
});

// O aviso some assim que a pessoa começa a digitar
campoLogin.addEventListener('input', function () {
  marcarCampo(campoLogin, erroLogin, false);
});
campoSenha.addEventListener('input', function () {
  marcarCampo(campoSenha, erroSenha, false);
});

// 3. Aviso de Caps Lock ligado enquanto digita a senha
campoSenha.addEventListener('keyup', function (evento) {
  if (evento.getModifierState('CapsLock')) {
    avisoCaps.style.display = 'block';
  } else {
    avisoCaps.style.display = 'none';
  }
});
