// Pede confirmação antes de enviar qualquer formulário de exclusão da página
const formulariosExcluir = document.querySelectorAll('.form-excluir');

for (const formulario of formulariosExcluir) {
  formulario.addEventListener('submit', function (evento) {
    const certeza = confirm('Tem certeza que quer excluir? Não dá para desfazer.');
    if (!certeza) {
      evento.preventDefault();   // cancela o envio do formulário
    }
  });
}
