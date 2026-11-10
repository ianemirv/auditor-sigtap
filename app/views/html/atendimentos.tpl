<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atendimentos — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='atendimentos')

  <main>
    <div class="titulo-pagina">
      <h1>Atendimentos</h1>
      <a class="botao" href="/atendimentos/novo">+ Novo atendimento</a>
    </div>

    % if len(linhas) == 0:
      <p class="vazio">Nenhum atendimento cadastrado ainda.</p>
    % else:
      <table>
        <thead>
          <tr>
            <th>Nº</th>
            <th>Data</th>
            <th>Texto clínico</th>
            <th>Faturados</th>
            <th>Situação</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          % for linha in linhas:
            % atendimento = linha['atendimento']
            <tr>
              <td>{{atendimento.id}}</td>
              <td class="nao-quebra">{{atendimento.data}}</td>
              <td>{{atendimento.resumo()}}</td>
              <td>{{len(atendimento.faturados)}}</td>
              <td>
                % if linha['alertas'] > 0:
                  <span class="selo selo-alerta">{{linha['alertas']}} não faturado(s)</span>
                % end
                % if linha['avisos'] > 0:
                  <span class="selo selo-aviso">{{linha['avisos']}} sem evidência</span>
                % end
                % if linha['alertas'] == 0 and linha['avisos'] == 0:
                  <span class="selo selo-ok">OK</span>
                % end
              </td>
              <td class="acoes">
                <a href="/atendimentos/{{atendimento.id}}">Ver</a>
                <a href="/atendimentos/{{atendimento.id}}/editar">Editar</a>
                <form class="form-excluir" method="POST" action="/atendimentos/{{atendimento.id}}/excluir">
                  <button type="submit" class="botao-texto perigo">Excluir</button>
                </form>
              </td>
            </tr>
          % end
        </tbody>
      </table>
    % end
  </main>

  <script src="/static/js/confirmar_exclusao.js"></script>
</body>
</html>
