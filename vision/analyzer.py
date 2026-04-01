def analisar():
    print("Analisando estrutura...")

    # SIMULAÇÃO (depois vamos pegar do gráfico)
    tendencia = "ALTA"
    ultimo_topo = 2050
    ultimo_fundo = 2000
    preco_atual = 2030

    if tendencia == "ALTA" and preco_atual > ultimo_fundo:
        direcao = "BUY"
    else:
        direcao = "SELL"

    return {
        "direcao": direcao,
        "entrada": preco_atual,
        "stop": ultimo_fundo,
        "tp": ultimo_topo
    }
