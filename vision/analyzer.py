import MetaTrader5 as mt5
import pandas as pd

def analisar():

    print("Conectando ao MT5...")

    if not mt5.initialize():
        return {"erro": "Erro ao conectar MT5"}

    symbol = "XAUUSD"

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)

    if rates is None:
        return {"erro": "Erro ao pegar dados"}

    df = pd.DataFrame(rates)

    # ===============================
    # 🔹 ESTRUTURA (BOS)
    # ===============================
    high = df['high']
    low = df['low']

    if high.iloc[-1] > high.iloc[-5]:
        estrutura = "ALTA"
    else:
        estrutura = "BAIXA"

    # ===============================
    # 🔹 LIQUIDEZ
    # ===============================
    topo = high.max()
    fundo = low.min()

    # ===============================
    # 🔹 PREÇO ATUAL
    # ===============================
    preco = df['close'].iloc[-1]

    # ===============================
    # 🔹 DECISÃO
    # ===============================
    if estrutura == "ALTA":
        direcao = "BUY"
        entrada = preco
        stop = fundo
        tp = entrada + (entrada - stop) * 2

    else:
        direcao = "SELL"
        entrada = preco
        stop = topo
        tp = entrada - (stop - entrada) * 2

    return {
        "direcao": direcao,
        "entrada": round(entrada, 2),
        "stop": round(stop, 2),
        "tp": round(tp, 2),
        "estrutura": estrutura
    }
