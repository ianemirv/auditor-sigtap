class AnalisadorFaturamento:
    """Compara o que o texto mostra com o que foi faturado."""

    def comparar(self, sugestoes, faturados):
        codigos_sugeridos = []
        for sugestao in sugestoes:
            codigos_sugeridos.append(sugestao.procedimento.codigo)

        # Está no texto, mas não foi faturado -> alerta de subfaturamento
        nao_faturados = []
        for sugestao in sugestoes:
            if sugestao.procedimento.codigo not in faturados:
                nao_faturados.append(sugestao)

        # Foi faturado, mas o texto não mostra -> aviso para conferir
        sem_evidencia = []
        for codigo in faturados:
            if codigo not in codigos_sugeridos:
                sem_evidencia.append(codigo)

        # Devolve as duas listas de uma vez
        return nao_faturados, sem_evidencia
