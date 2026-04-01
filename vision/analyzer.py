def analisar():
    print("Analisando estrutura avançada...")

    # SIMULAÇÃO (depois será gráfico real)
    dados = {
        "tendencia": "ALTA",
        "topo_anterior": 2050,
        "fundo_anterior": 2000,
        "preco_atual": 2030,
        "liquidez_varrida": True
    }

    # lógica mais inteligente
    if dados["tendencia"] == "ALTA" and dados["liquidez_varrida"]:
        direcao = "BUY"
        entrada = dados["preco_atual"]
        stop = dados["fundo_anterior"]
        tp = dados["topo_anterior"]
        motivo = "Tendência de alta + liquidez varrida"
    else:
        direcao = "SELL"
        entrada = dados["preco_atual"]
        stop = dados["topo_anterior"]
        tp = dados["fundo_anterior"]
        motivo = "Possível reversão"

    return {
        "direcao": direcao,
        "entrada": entrada,
        "stop": stop,
        "tp": tp,
        "motivo": motivo
    }
