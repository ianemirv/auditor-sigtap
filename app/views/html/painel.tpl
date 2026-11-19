<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='painel')

  <main>
    <h1 id="saudacao" data-nome="{{usuario.nome}}">Olá, {{usuario.nome}}</h1>
    <p class="explicacao">
      Você entrou como <strong>{{usuario.tipo()}}</strong>.
      Este painel só aparece para quem fez login.
    </p>

    <!-- Números do sistema: o painel.js faz eles subirem de 0 até o valor -->
    <div class="cartoes-numeros">
      <a class="cartao-numero" href="/atendimentos">
        <span class="numero" data-numero="{{total_atendimentos}}">{{total_atendimentos}}</span>
        <span>atendimentos cadastrados</span>
      </a>
      <a class="cartao-numero cartao-alerta" href="/atendimentos">
        <span class="numero" data-numero="{{com_alerta}}">{{com_alerta}}</span>
        <span>atendimentos com alerta</span>
      </a>
      <a class="cartao-numero cartao-alerta" href="/atendimentos">
        <span class="numero" data-numero="{{total_alertas}}">{{total_alertas}}</span>
        <span>procedimentos não faturados</span>
      </a>
      <a class="cartao-numero" href="/atendimentos">
        <span class="numero" data-numero="{{meus}}">{{meus}}</span>
        <span>cadastrados por você</span>
      </a>
    </div>

    <div class="duas-colunas">
      <section class="caixa">
        <h2>Últimos alertas de subfaturamento</h2>
        % if len(ultimos_alertas) == 0:
          <p class="tudo-certo">Nenhum alerta. Tudo o que está nos textos foi faturado.</p>
        % end
        % for item in ultimos_alertas:
          % atendimento = item['atendimento']
          <a class="item-alerta" href="/atendimentos/{{atendimento.id}}">
            <strong>Atendimento nº {{atendimento.id}}</strong>
            <small>{{atendimento.data}}</small>
            % for sugestao in item['nao_faturados']:
              <span class="selo selo-alerta">{{sugestao.procedimento.nome}}</span>
            % end
          </a>
        % end
      </section>

      <section class="caixa">
        <h2>O que você pode fazer</h2>
        <ul class="permissoes">
          <li class="sim">Cadastrar, editar e excluir atendimentos</li>
          <li class="sim">Ver as sugestões e os alertas</li>
          <li class="sim">Consultar o catálogo SIGTAP ({{total_procedimentos}} procedimentos)</li>
          <li class="{{'sim' if usuario.pode_editar_catalogo() else 'nao'}}">Editar o catálogo SIGTAP</li>
          <li class="{{'sim' if usuario.pode_gerenciar_usuarios() else 'nao'}}">Gerenciar usuários</li>
        </ul>

        <h2>Atalhos</h2>
        <div class="botoes atalhos">
          <a class="botao" href="/atendimentos/novo">+ Novo atendimento</a>
          % if usuario.pode_editar_catalogo():
            <a class="botao-secundario" href="/procedimentos/novo">+ Procedimento</a>
          % end
          % if usuario.pode_gerenciar_usuarios():
            <a class="botao-secundario" href="/usuarios">Usuários ({{total_usuarios}})</a>
          % end
        </div>
      </section>
    </div>
  </main>

  <script src="/static/js/painel.js"></script>
</body>
</html>
