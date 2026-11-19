<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Entrar — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/login.css">
</head>
<body>

  <main class="caixa-login">
    <h1>Auditor SIGTAP</h1>
    <p class="subtitulo">Entre com a sua conta para auditar os atendimentos.</p>

    % if erro is not None:
      <p class="erro-servidor">{{erro}}</p>
    % end

    <form id="form-login" method="POST" action="/login">

      <label for="login">Login</label>
      <input id="login" name="login" type="text" autocomplete="username" autofocus>
      <span id="erro-login" class="erro-campo escondido">Digite o seu login.</span>

      <label for="senha">Senha</label>
      <div class="campo-senha">
        <input id="senha" name="senha" type="password" autocomplete="current-password">
        <button id="botao-mostrar" type="button">Mostrar</button>
      </div>
      <span id="erro-senha" class="erro-campo escondido">Digite a sua senha.</span>
      <span id="aviso-caps" class="aviso-caps escondido">Caps Lock está ligado.</span>

      <button type="submit" class="botao-entrar">Entrar</button>
    </form>

    <p class="rodape-login">
      <a href="/">← Voltar para a apresentação</a>
    </p>
  </main>

  <script src="/static/js/login.js"></script>
</body>
</html>
