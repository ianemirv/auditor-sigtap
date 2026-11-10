<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atendimento nº {{atendimento.id}} — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='')

  <main>
    <div class="titulo-pagina">
      <h1>Atendimento nº {{atendimento.id}}</h1>
      <div class="botoes">
        <a class="botao-secundario" href="/atendimentos/{{atendimento.id}}/editar">Editar</a>
        <form class="form-excluir" method="POST" action="/atendimentos/{{atendimento.id}}/excluir">
          <button type="submit" class="botao perigo">Excluir</button>
        </form>
      </div>
    </div>
    <p class="data">Cadastrado em {{atendimento.data}}</p>

    <!-- Alertas primeiro: é o que o auditor precisa ver -->
    % for sugestao in nao_faturados:
      <p class="alerta">
        <strong>Possível subfaturamento:</strong>
        {{sugestao.procedimento.nome}} ({{sugestao.procedimento.codigo}})
        aparece no texto e não foi faturado.
      </p>
    % end
    % for item in sem_evidencia:
      <p class="aviso">
        <strong>Conferir:</strong>
        {{item['nome']}} ({{item['codigo']}}) foi faturado, mas o texto não menciona.
      </p>
    % end
    % if len(nao_faturados) == 0 and len(sem_evidencia) == 0:
      <p class="tudo-certo">Tudo certo: o que está no texto foi faturado.</p>
    % end

    <section class="caixa">
      <div class="titulo-caixa">
        <h2>Texto clínico</h2>
        <button id="botao-destacar" class="botao-secundario" type="button">Destacar palavras-chave</button>
      </div>
      <p id="texto-clinico" class="texto-clinico" data-palavras="{{'|'.join(palavras)}}">{{atendimento.texto}}</p>
    </section>

    <div class="duas-colunas">
      <section class="caixa">
        <h2>Sugestões do sistema</h2>
        % if len(sugestoes) == 0:
          <p class="vazio">Nenhum procedimento do catálogo foi encontrado no texto.</p>
        % end
        % for sugestao in sugestoes:
          <div class="sugestao">
            <div class="sugestao-topo">
              <span>{{sugestao.procedimento.nome}}</span>
              <span class="pontos">{{sugestao.porcentagem}}%</span>
            </div>
            <div class="barra">
              <div class="barra-cheia" style="width: {{sugestao.porcentagem}}%"></div>
            </div>
            <small>{{sugestao.procedimento.codigo}} · achou: {{', '.join(sugestao.palavras_encontradas)}}</small>
          </div>
        % end
      </section>

      <section class="caixa">
        <h2>Faturados pelo codificador</h2>
        % if len(faturados) == 0:
          <p class="vazio">Nenhum procedimento faturado.</p>
        % end
        <ul class="lista-faturados">
          % for item in faturados:
            <li><span class="codigo">{{item['codigo']}}</span> {{item['nome']}}</li>
          % end
        </ul>
      </section>
    </div>

    <p><a href="/atendimentos">← Voltar para a lista</a></p>
  </main>

  <script src="/static/js/confirmar_exclusao.js"></script>
  <script src="/static/js/atendimento_detalhe.js"></script>
</body>
</html>
