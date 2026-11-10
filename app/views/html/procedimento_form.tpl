<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{titulo}} — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='procedimentos')

  <main>
    <h1>{{titulo}}</h1>

    % if erro is not None:
      <p class="alerta">{{erro}}</p>
    % end

    <form id="form-procedimento" class="formulario" method="POST" action="{{acao}}">

      <label for="codigo">Código SIGTAP</label>
      % if procedimento is None:
        <input id="codigo" name="codigo" type="text" placeholder="02.02.02.038-0">
      % else:
        <input id="codigo" type="text" value="{{procedimento.codigo}}" readonly>
        <small>O código não muda. Para trocar, exclua e cadastre de novo.</small>
      % end

      <label for="nome">Nome oficial</label>
      <input id="nome" name="nome" type="text" placeholder="Hemograma completo"
        value="{{procedimento.nome if procedimento is not None else ''}}">

      <label for="palavras_chave">Palavras-chave (separadas por vírgula)</label>
      <input id="palavras_chave" name="palavras_chave" type="text" placeholder="hemograma, hmg"
        value="{{', '.join(procedimento.palavras_chave) if procedimento is not None else ''}}">
      <div id="previa" class="previa"></div>

      <p id="erro-procedimento" class="erro escondido">Preencha todos os campos.</p>

      <div class="botoes">
        <button type="submit" class="botao">Salvar</button>
        <a class="botao-secundario" href="/procedimentos">Cancelar</a>
      </div>
    </form>
  </main>

  <script src="/static/js/procedimento_form.js"></script>
</body>
</html>
