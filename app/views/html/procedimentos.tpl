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
      <a class="botao" href="/procedimentos/novo">+ Novo procedimento</a>
    </div>
    <p class="explicacao">
      Recorte da tabela SIGTAP usado pelo sistema. As palavras-chave são as que
      o classificador procura nos textos clínicos.
    </p>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nome</th>
          <th>Palavras-chave</th>
          <th>Ações</th>
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
            <td class="acoes">
              <a href="/procedimentos/{{procedimento.codigo}}/editar">Editar</a>
              <form class="form-excluir" method="POST" action="/procedimentos/{{procedimento.codigo}}/excluir">
                <button type="submit" class="botao-texto perigo">Excluir</button>
              </form>
            </td>
          </tr>
        % end
      </tbody>
    </table>
  </main>

  <script src="/static/js/confirmar_exclusao.js"></script>
</body>
</html>
