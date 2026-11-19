<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo SIGTAP — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='procedimentos')

  <main>
    <div class="titulo-pagina">
      <h1>Catálogo SIGTAP</h1>
      % if usuario.pode_editar_catalogo():
        <a class="botao" href="/procedimentos/novo">+ Novo procedimento</a>
      % end
    </div>
    <p class="explicacao">
      Recorte da tabela SIGTAP usado pelo sistema. As palavras-chave são as que
      o classificador procura nos textos clínicos.
    </p>
    % if not usuario.pode_editar_catalogo():
      <p class="aviso">Você pode consultar o catálogo. Só o administrador cadastra, edita ou exclui procedimentos.</p>
    % end

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nome</th>
          <th>Palavras-chave</th>
          % if usuario.pode_editar_catalogo():
            <th>Ações</th>
          % end
        </tr>
      </thead>
      <tbody>
        % for procedimento in procedimentos:
          <tr>
            <td class="codigo nao-quebra">{{procedimento.codigo}}</td>
            <td>{{procedimento.nome}}</td>
            <td>
              % for palavra in procedimento.palavras_chave:
                <span class="etiqueta">{{palavra}}</span>
              % end
            </td>
            % if usuario.pode_editar_catalogo():
              <td class="acoes">
                <a href="/procedimentos/{{procedimento.codigo}}/editar">Editar</a>
                <form class="form-excluir" method="POST" action="/procedimentos/{{procedimento.codigo}}/excluir">
                  <button type="submit" class="botao-texto perigo">Excluir</button>
                </form>
              </td>
            % end
          </tr>
        % end
      </tbody>
    </table>
  </main>

  <script src="/static/js/confirmar_exclusao.js"></script>
</body>
</html>
