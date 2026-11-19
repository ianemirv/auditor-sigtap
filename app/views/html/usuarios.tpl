<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Usuários — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='usuarios')

  <main>
    <div class="titulo-pagina">
      <h1>Usuários</h1>
      <a class="botao" href="/usuarios/novo">+ Novo usuário</a>
    </div>
    <p class="explicacao">
      Codificadores cadastram atendimentos. Administradores também editam o catálogo
      e cuidam dos usuários. As senhas ficam guardadas só como hash.
    </p>

    % if erro is not None:
      <p class="alerta">{{erro}}</p>
    % end

    <table>
      <thead>
        <tr>
          <th>Nº</th>
          <th>Nome</th>
          <th>Login</th>
          <th>Tipo</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        % for pessoa in usuarios:
          <tr>
            <td>{{pessoa.id}}</td>
            <td>
              {{pessoa.nome}}
              % if pessoa.id == usuario.id:
                <small class="vazio">(você)</small>
              % end
            </td>
            <td class="codigo">{{pessoa.login}}</td>
            <td><span class="selo-tipo selo-{{pessoa.tipo()}}">{{pessoa.tipo().capitalize()}}</span></td>
            <td class="acoes">
              <a href="/usuarios/{{pessoa.id}}/editar">Editar</a>
              % if pessoa.id != usuario.id:
                <form class="form-excluir" method="POST" action="/usuarios/{{pessoa.id}}/excluir">
                  <button type="submit" class="botao-texto perigo">Excluir</button>
                </form>
              % end
            </td>
          </tr>
        % end
      </tbody>
    </table>
  </main>

  <script src="/static/js/confirmar_exclusao.js"></script>
</body>
</html>
