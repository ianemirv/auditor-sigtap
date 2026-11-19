<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{titulo}} — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='usuarios')

  <main>
    <h1>{{titulo}}</h1>

    % if erro is not None:
      <p class="alerta">{{erro}}</p>
    % end

    <!-- data-senha-obrigatoria: no cadastro a senha é obrigatória; na edição, não -->
    <form id="form-usuario" class="formulario" method="POST" action="{{acao}}"
      data-senha-obrigatoria="{{'sim' if editado is None else 'nao'}}">

      <label for="nome">Nome</label>
      <input id="nome" name="nome" type="text" placeholder="Marina Lopes"
        value="{{editado.nome if editado is not None else ''}}">

      <label for="login">Login</label>
      % if editado is None:
        <input id="login" name="login" type="text" placeholder="marina">
        <small>Sem espaços. É o que a pessoa digita para entrar.</small>
      % else:
        <input id="login" type="text" value="{{editado.login}}" readonly>
        <small>O login não muda.</small>
      % end

      <fieldset>
        <legend>Tipo</legend>
        % if editado is not None and editado.id == usuario.id:
          <input type="hidden" name="tipo" value="{{editado.tipo()}}">
          <p>{{editado.tipo().capitalize()}} <small>(você não pode mudar o seu próprio tipo)</small></p>
        % else:
          <label class="opcao">
            <input type="radio" name="tipo" value="codificador"
              {{'checked' if editado is None or editado.tipo() == 'codificador' else ''}}>
            <strong>Codificador</strong> — cadastra e confere atendimentos
          </label>
          <label class="opcao">
            <input type="radio" name="tipo" value="administrador"
              {{'checked' if editado is not None and editado.tipo() == 'administrador' else ''}}>
            <strong>Administrador</strong> — também edita o catálogo e os usuários
          </label>
        % end
      </fieldset>

      <label for="senha">{{'Senha' if editado is None else 'Nova senha'}}</label>
      <div class="campo-senha">
        <input id="senha" name="senha" type="password" autocomplete="new-password">
        <button id="botao-mostrar" class="botao-secundario" type="button">Mostrar</button>
      </div>
      % if editado is not None:
        <small>Deixe em branco para manter a senha atual.</small>
      % end

      <label for="confirmar">Repita a senha</label>
      <input id="confirmar" name="confirmar" type="password" autocomplete="new-password">
      <span id="situacao-senha" class="contador"></span>

      <p id="erro-usuario" class="erro escondido"></p>

      <div class="botoes">
        <button type="submit" class="botao">Salvar</button>
        <a class="botao-secundario" href="/usuarios">Cancelar</a>
      </div>
    </form>
  </main>

  <script src="/static/js/usuario_form.js"></script>
</body>
</html>
