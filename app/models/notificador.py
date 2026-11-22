import json


class NotificadorAuditoria:
    """Guarda as conexões WebSocket abertas e manda mensagens para todas.

    Cada painel de auditoria aberto no navegador é uma conexão.
    Quando um atendimento é salvo, o controller chama enviar() e
    a mensagem chega na hora em todos os painéis, sem recarregar a página.
    """

    def __init__(self):
        self._conexoes = []   # privado: só esta classe mexe na lista

    def conectar(self, conexao):
        self._conexoes.append(conexao)

    def desconectar(self, conexao):
        if conexao in self._conexoes:
            self._conexoes.remove(conexao)

    def total_conectados(self):
        return len(self._conexoes)

    def enviar(self, dados):
        """Transforma os dados em texto JSON e manda para todas as conexões.

        Se uma conexão caiu (o navegador fechou), o envio dá erro.
        Essa conexão é anotada e tirada da lista no final.
        """
        texto = json.dumps(dados, ensure_ascii=False)
        caidas = []
        # list(...) faz uma cópia: assim a lista original pode mudar sem problema
        for conexao in list(self._conexoes):
            try:
                conexao.send(texto)
            except Exception:
                caidas.append(conexao)
        for conexao in caidas:
            self.desconectar(conexao)

    def recusar(self, conexao):
        """Avisa o navegador que ele não tem permissão e fecha a conexão."""
        conexao.send(json.dumps({'tipo': 'negado'}))
        conexao.close()
