<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Auditoria ao vivo — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='auditoria')

  <main>
    <div class="titulo-pagina">
      <h1>Auditoria em tempo real</h1>
      <!-- O auditoria.js troca a cor e o texto conforme a conexão -->
      <span id="estado-conexao" class="estado estado-conectando">
        <span id="texto-estado">Conectando...</span>
      </span>
    </div>
    <p class="explicacao">
      Deixe esta página aberta. Quando alguém salvar um atendimento com procedimento
      citado no texto e não faturado, o alerta aparece aqui na hora, sem recarregar.
    </p>

    <div class="cartoes-numeros">
      <div class="cartao-numero cartao-alerta">
        <span class="numero" id="contador-fila">{{len(alertas)}}</span>
        <span>atendimentos na fila de auditoria</span>
      </div>
      <div class="cartao-numero cartao-alerta">
        <span class="numero" id="contador-procedimentos">{{total_procedimentos}}</span>
        <span>procedimentos não faturados</span>
      </div>
      <div class="cartao-numero">
        <span class="numero" id="contador-ao-vivo">0</span>
        <span>alertas recebidos ao vivo</span>
      </div>
    </div>

    <div class="duas-colunas colunas-auditoria">
      <section class="caixa coluna-fila">
        <h2>Fila de auditoria</h2>
        <p id="fila-vazia" class="tudo-certo {{'escondido' if len(alertas) > 0 else ''}}">
          Nenhum alerta. Tudo o que está nos textos foi faturado.
        </p>

        <div id="fila">
          % for alerta in alertas:
            <article class="cartao-auditoria" data-id="{{alerta['id']}}"
                     data-procedimentos="{{len(alerta['procedimentos'])}}">
              <div class="cartao-topo">
                <strong>Atendimento nº {{alerta['id']}}</strong>
                <span class="selo selo-acao">{{alerta['acao']}}</span>
              </div>
              <p class="cartao-quem">por {{alerta['quem']}} · {{alerta['horario']}}</p>
              <p class="cartao-resumo">{{alerta['resumo']}}</p>
              <p class="cartao-legenda">Citado no texto e não faturado:</p>
              <div class="cartao-selos">
                % for procedimento in alerta['procedimentos']:
                  <span class="selo selo-alerta"
                        title="{{procedimento['codigo']}} · {{procedimento['porcentagem']}}% de confiança">{{procedimento['nome']}}</span>
                % end
              </div>
              <a class="cartao-link" href="/atendimentos/{{alerta['id']}}">Abrir atendimento →</a>
            </article>
          % end
        </div>
      </section>

      <section class="caixa coluna-atividade">
        <h2>Atividade ao vivo</h2>
        <p id="atividade-vazia" class="vazio">
          Nada ainda. Cada atendimento salvo por qualquer usuário aparece aqui.
        </p>
        <ul id="atividade" class="atividade"></ul>
      </section>
    </div>
  </main>

  <script src="/static/js/auditoria.js"></script>
</body>
</html>
