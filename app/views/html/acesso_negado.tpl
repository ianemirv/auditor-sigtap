<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Acesso negado — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='')

  <main>
    <div class="caixa negado">
      <p class="codigo-erro">403</p>
      <h1>Acesso negado</h1>
      % if usuario is not None:
        <p>
          Você entrou como <strong>{{usuario.tipo()}}</strong> e não tem permissão
          para abrir esta página. Fale com um administrador se precisar.
        </p>
      % else:
        <p>Você precisa entrar no sistema para abrir esta página.</p>
      % end
      <p><a class="botao" href="/painel">Voltar para o painel</a></p>
    </div>
  </main>

</body>
</html>
