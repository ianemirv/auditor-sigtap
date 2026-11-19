<header class="topo">
  <a class="marca" href="/painel">Auditor SIGTAP</a>
  <nav>
    <a href="/painel" class="{{'ativo' if ativo == 'painel' else ''}}">Painel</a>
    <a href="/atendimentos" class="{{'ativo' if ativo == 'atendimentos' else ''}}">Atendimentos</a>
    <a href="/atendimentos/novo" class="{{'ativo' if ativo == 'novo' else ''}}">Novo atendimento</a>
    <a href="/procedimentos" class="{{'ativo' if ativo == 'procedimentos' else ''}}">Catálogo SIGTAP</a>
    % if usuario is not None and usuario.pode_gerenciar_usuarios():
      <a href="/usuarios" class="{{'ativo' if ativo == 'usuarios' else ''}}">Usuários</a>
    % end
  </nav>
  % if usuario is not None:
    <div class="usuario-logado">
      <span>{{usuario.nome}}</span>
      <span class="selo-tipo selo-{{usuario.tipo()}}">{{usuario.tipo().capitalize()}}</span>
      <a class="botao-sair" href="/logout">Sair</a>
    </div>
  % end
</header>
