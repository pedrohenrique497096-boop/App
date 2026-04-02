import MetaTrader5 as mt5
import pandas as pd

SYMBOL = "XAUUSDm"
CANDLES = 500


# =========================
# 🔌 CONEXÃO MT5
# =========================
def connect():
    return mt5.initialize()


def get_data(tf):
    rates = mt5.copy_rates_from_pos(SYMBOL, tf, 0, CANDLES)
    if rates is None:
        return None
    return pd.DataFrame(rates)


# =========================
# 📊 ESTRUTURA (BOS / TREND)
# =========================
def structure(df):
    highs = df["high"].values
    lows = df["low"].values

    if highs[-1] > highs[-5]:
        return "ALTA", "BOS"
    elif lows[-1] < lows[-5]:
        return "BAIXA", "BOS"
    else:
        return "RANGE", "NONE"


# =========================
# 💧 LIQUIDEZ (SWEEP)
# =========================
def liquidity(df):
    last = df.iloc[-1]

    if last["low"] < df["low"].iloc[-5] and last["close"] > last["low"]:
        return "SSL_SWEEP"

    if last["high"] > df["high"].iloc[-5] and last["close"] < last["high"]:
        return "BSL_SWEEP"

    return "NONE"


# =========================
# 📉 FVG
# =========================
def fvg(df):
    c1 = df.iloc[-3]
    c3 = df.iloc[-1]

    if c3["low"] > c1["high"]:
        return "BULL"

    if c3["high"] < c1["low"]:
        return "BEAR"

    return "NONE"


# =========================
# 📦 ORDER BLOCK (simples)
# =========================
def order_block(df):
    last = df.iloc[-2]

    if last["close"] < last["open"]:
        return "BULL_OB"

    if last["close"] > last["open"]:
        return "BEAR_OB"

    return "NONE"


# =========================
# 🎯 ANALISE POR TF
# =========================
def analyze_tf(df):
    trend, _ = structure(df)
    liq = liquidity(df)
    fvg_type = fvg(df)
    ob = order_block(df)

    score_buy = 0
    score_sell = 0

    if trend == "ALTA":
        score_buy += 20
    if trend == "BAIXA":
        score_sell += 20

    if liq == "SSL_SWEEP":
        score_buy += 15
    if liq == "BSL_SWEEP":
        score_sell += 15

    if fvg_type == "BULL":
        score_buy += 10
    if fvg_type == "BEAR":
        score_sell += 10

    if ob == "BULL_OB":
        score_buy += 8
    if ob == "BEAR_OB":
        score_sell += 8

    if score_buy > score_sell and score_buy > 25:
        direction = "BUY"
    elif score_sell > score_buy and score_sell > 25:
        direction = "SELL"
    else:
        direction = "NEUTRO"

    return {
        "direction": direction,
        "score_buy": score_buy,
        "score_sell": score_sell
    }


# =========================
# 🔥 MODO SNIPER
# =========================
def analisar():
    if not connect():
        return {"erro": "Erro ao conectar MT5"}

    mt5.symbol_select(SYMBOL, True)

    # =========================
    # 🔵 DIREÇÃO H1
    # =========================
    df_h1 = get_data(mt5.TIMEFRAME_H1)
    if df_h1 is None:
        return {"erro": "Sem dados H1"}

    h1 = analyze_tf(df_h1)
    direcao_macro = h1["direction"]

    if direcao_macro == "NEUTRO":
        return {
            "direcao": "NEUTRO",
            "motivo": "Sem tendência H1",
            "modo": "SNIPER"
        }

    # =========================
    # 🟡 ENTRADA M5
    # =========================
    df_m5 = get_data(mt5.TIMEFRAME_M5)
    if df_m5 is None:
        return {"erro": "Sem dados M5"}

    liq = liquidity(df_m5)
    fvg_type = fvg(df_m5)

    price = df_m5["close"].iloc[-1]

    # =========================
    # 🔥 BUY
    # =========================
    if direcao_macro == "BUY":

        if liq == "SSL_SWEEP" and fvg_type == "BULL":

            stop = df_m5["low"].iloc[-2]
            tp = price + ((price - stop) * 2)

            return {
                "direcao": "BUY",
                "entrada": round(price, 2),
                "stop": round(stop, 2),
                "tp": round(tp, 2),
                "motivo": "H1 alta + sweep + FVG",
                "modo": "SNIPER"
            }

    # =========================
    # 🔥 SELL
    # =========================
    if direcao_macro == "SELL":

        if liq == "BSL_SWEEP" and fvg_type == "BEAR":

            stop = df_m5["high"].iloc[-2]
            tp = price - ((stop - price) * 2)

            return {
                "direcao": "SELL",
                "entrada": round(price, 2),
                "stop": round(stop, 2),
                "tp": round(tp, 2),
                "motivo": "H1 baixa + sweep + FVG",
                "modo": "SNIPER"
            }

    # =========================
    # ❌ SEM TRADE
    # =========================
    return {
        "direcao": "NEUTRO",
        "motivo": "Sem confirmação sniper",
        "modo": "SNIPER"
        }
