<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{titulo}} — Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/sistema.css">
</head>
<body>

  % include('app/views/html/menu', ativo='novo' if atendimento is None else '')

  <main>
    <h1>{{titulo}}</h1>

    <form id="form-atendimento" class="formulario" method="POST" action="{{acao}}">

      <label for="texto">Texto clínico</label>
      <textarea id="texto" name="texto" rows="6"
        placeholder="Ex.: Paciente com dor abdominal. Realizados USG de abdome e hemograma.">{{atendimento.texto if atendimento is not None else ''}}</textarea>
      <div class="linha-info">
        <span id="erro-texto" class="erro escondido">Escreva o texto clínico antes de salvar.</span>
        <span id="contador" class="contador">0 caracteres</span>
      </div>

      <fieldset>
        <legend>Procedimentos faturados <span id="total-marcados" class="contador"></span></legend>
        % for procedimento in procedimentos:
          <label class="opcao">
            <input type="checkbox" name="faturados" value="{{procedimento.codigo}}"
              {{'checked' if atendimento is not None and procedimento.codigo in atendimento.faturados else ''}}>
            <span class="codigo">{{procedimento.codigo}}</span>
            {{procedimento.nome}}
          </label>
        % end
      </fieldset>

      <div class="botoes">
        <button type="submit" class="botao">Salvar e analisar</button>
        <a class="botao-secundario" href="/atendimentos">Cancelar</a>
      </div>
    </form>
  </main>

  <script src="/static/js/atendimento_form.js"></script>
</body>
</html>
