import MetaTrader5 as mt5
import pandas as pd

def analisar():

    print("Modo MT5 (SMC PRO)")

    if not mt5.initialize():
        return {"erro": "Erro MT5"}

    symbol = "XAUUSDm"
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 200)

    df = pd.DataFrame(rates)

    # 🔥 PREÇO ATUAL
    preco = df['close'].iloc[-1]

    # 🔥 ESTRUTURA (BOS)
    topo_anterior = df['high'].iloc[-20:-1].max()
    fundo_anterior = df['low'].iloc[-20:-1].min()

    if preco > topo_anterior:
        estrutura = "BOS_ALTA"
    elif preco < fundo_anterior:
        estrutura = "BOS_BAIXA"
    else:
        estrutura = "RANGE"

    # 🔥 LIQUIDEZ
    liquidez_topo = df['high'].rolling(10).max().iloc[-1]
    liquidez_fundo = df['low'].rolling(10).min().iloc[-1]

    # 🔥 IMBALANCE (FVG SIMPLES)
    fvg = abs(df['close'].iloc[-1] - df['open'].iloc[-1])

    # 🔥 DECISÃO SMC
    if estrutura == "BOS_ALTA" and preco < liquidez_topo:
        direcao = "BUY"
        entrada = preco
        stop = liquidez_fundo
        tp = liquidez_topo
        motivo = "BOS + Liquidez"

    elif estrutura == "BOS_BAIXA" and preco > liquidez_fundo:
        direcao = "SELL"
        entrada = preco
        stop = liquidez_topo
        tp = liquidez_fundo
        motivo = "BOS + Liquidez"

    else:
        direcao = "NEUTRO"
        entrada = stop = tp = 0
        motivo = "Sem estrutura"

    return {
        "direcao": direcao,
        "entrada": round(entrada, 2),
        "stop": round(stop, 2),
        "tp": round(tp, 2),
        "estrutura": estrutura,
        "liquidez": round(liquidez_topo - liquidez_fundo, 2),
        "imbalance": round(fvg, 2),
        "motivo": motivo,
        "modo": "SMC PRO"
    }
