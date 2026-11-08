<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Auditor SIGTAP</title>
  <link rel="stylesheet" href="/static/css/index.css">
</head>
<body>

  <header>
    <h1>Auditor SIGTAP</h1>
    <p>Encontra procedimentos do SUS que foram feitos, mas não foram cobrados.</p>
  </header>

  <main>

    <section>
      <h2>O problema</h2>
      <p>
        Todo atendimento no SUS gera um texto escrito pelo médico no prontuário.
        Para o hospital receber pelo atendimento, cada procedimento feito precisa
        ser informado com um código da tabela SIGTAP. Se alguém esquece um
        procedimento, o hospital fez o serviço e não recebe por ele.
        Isso se chama <strong>subfaturamento</strong>.
      </p>
    </section>

    <section>
      <h2>O que é a tabela SIGTAP</h2>
      <p>
        É a lista oficial de procedimentos do SUS, mantida pelo DATASUS.
        Cada procedimento tem um código, por exemplo:
        <strong>02.02.02.038-0 — Hemograma completo</strong>.
      </p>
    </section>

    <section>
      <h2>Como funciona</h2>
      <div class="cartoes">
        <div class="cartao">
          <h3>1. Cadastro</h3>
          <p>O codificador cola o texto clínico e informa o que foi cobrado.</p>
        </div>
        <div class="cartao">
          <h3>2. Leitura</h3>
          <p>O sistema procura no texto os procedimentos da tabela SIGTAP.</p>
        </div>
        <div class="cartao">
          <h3>3. Comparação</h3>
          <p>O que está no texto e não foi cobrado vira um alerta.</p>
        </div>
        <div class="cartao">
          <h3>4. Auditoria</h3>
          <p>O administrador vê os alertas num painel.</p>
        </div>
      </div>
    </section>

    <section>
      <h2>Exemplo</h2>
      <button id="botao-exemplo">Ver exemplo</button>

      <div id="exemplo" class="escondido">
        <p class="texto-clinico">
          "Paciente com dor abdominal. Realizados ultrassonografia de abdome
          e hemograma completo."
        </p>
        <p>Cobrado pelo codificador: <strong>Hemograma completo</strong></p>
        <button id="botao-analisar">Analisar</button>
      </div>

      <div id="resultado" class="escondido">
        <h3>Procedimentos encontrados no texto</h3>
        <ul>
          <li>Hemograma completo — cobrado</li>
          <li>Ultrassonografia de abdome — <strong>não cobrado</strong></li>
        </ul>
        <p class="alerta">
          Alerta: a ultrassonografia está no texto, mas não foi cobrada.
        </p>
      </div>
    </section>

  </main>

  <footer>
    <p>Ian — Orientação a Objetos — UnB</p>
  </footer>

  <script src="/static/js/index.js"></script>
</body>
</html>
