import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time

SYMBOL = "XAUUSDm"
CANDLES = 500

LAST_SIGNAL = {"dir": None, "time": 0}


def connect():
    return mt5.initialize()


def get_data(tf):
    rates = mt5.copy_rates_from_pos(SYMBOL, tf, 0, CANDLES)
    if rates is None:
        return None
    df = pd.DataFrame(rates)
    return df


# =========================
# 🔥 STRUCTURE (BOS / CHOCH)
# =========================
def structure(df):
    highs = df["high"].values
    lows = df["low"].values

    hh = highs[-1] > highs[-5]
    ll = lows[-1] < lows[-5]

    if hh and not ll:
        return "ALTA", "BOS"
    elif ll and not hh:
        return "BAIXA", "BOS"
    else:
        return "RANGE", "NONE"


# =========================
# 🔥 EQUAL HIGH / LOW
# =========================
def equal_levels(df):
    h1, h2 = df["high"].iloc[-1], df["high"].iloc[-2]
    l1, l2 = df["low"].iloc[-1], df["low"].iloc[-2]

    eqh = abs(h1 - h2) < 1.0
    eql = abs(l1 - l2) < 1.0

    return eqh, eql


# =========================
# 🔥 FVG + IFVG
# =========================
def fvg(df):
    c1 = df.iloc[-3]
    c3 = df.iloc[-1]

    if c3["low"] > c1["high"]:
        return "BULL", c3["low"], c1["high"]

    if c3["high"] < c1["low"]:
        return "BEAR", c1["low"], c3["high"]

    return "NONE", 0, 0


def ifvg(df):
    c1 = df.iloc[-3]
    c3 = df.iloc[-1]

    if c3["close"] < c1["high"]:
        return "IFVG_BEAR"

    if c3["close"] > c1["low"]:
        return "IFVG_BULL"

    return "NONE"


# =========================
# 🔥 ORDER BLOCKS (OB/BB/MB/RB)
# =========================
def order_blocks(df):
    last = df.iloc[-2]

    if last["close"] < last["open"]:
        return "BULL_OB"

    if last["close"] > last["open"]:
        return "BEAR_OB"

    return "NONE"


def breaker_block(df):
    if df["close"].iloc[-1] > df["high"].iloc[-5]:
        return "BULL_BREAKER"
    if df["close"].iloc[-1] < df["low"].iloc[-5]:
        return "BEAR_BREAKER"
    return "NONE"


def mitigation_block(df):
    if df["close"].iloc[-1] == df["open"].iloc[-1]:
        return "MITIGATION"
    return "NONE"


def rejection_block(df):
    candle = df.iloc[-1]
    body = abs(candle["close"] - candle["open"])
    wick = candle["high"] - candle["low"]

    if wick > body * 3:
        return "REJECTION"
    return "NONE"


# =========================
# 🔥 LIQUIDITY
# =========================
def liquidity(df):
    high = df["high"].iloc[-1]
    low = df["low"].iloc[-1]

    if high > df["high"].iloc[-5] and df["close"].iloc[-1] < high:
        return "BSL_SWEEP"

    if low < df["low"].iloc[-5] and df["close"].iloc[-1] > low:
        return "SSL_SWEEP"

    return "NONE"


# =========================
# 🔥 RANGE / IRL / ERL
# =========================
def range_liquidity(df):
    high = df["high"].max()
    low = df["low"].min()

    mid = (high + low) / 2

    price = df["close"].iloc[-1]

    if price > mid:
        return "ERL"
    else:
        return "IRL"


# =========================
# 🔥 LIQUIDITY VOID / IMBALANCE
# =========================
def imbalance(df):
    return abs(df["close"].iloc[-1] - df["open"].iloc[-1])


def liquidity_void(df):
    if abs(df["high"].iloc[-1] - df["low"].iloc[-1]) > 20:
        return "LV"
    return "NONE"


# =========================
# 🔥 MAIN ANALYSIS
# =========================
def analyze_tf(df):
    trend, bos = structure(df)
    eqh, eql = equal_levels(df)
    fvg_type, fvg_top, fvg_bot = fvg(df)
    ifvg_type = ifvg(df)

    ob = order_blocks(df)
    bb = breaker_block(df)
    mb = mitigation_block(df)
    rb = rejection_block(df)

    liq = liquidity(df)
    rl = range_liquidity(df)

    imb = imbalance(df)
    lv = liquidity_void(df)

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

    if bb == "BULL_BREAKER":
        score_buy += 10
    if bb == "BEAR_BREAKER":
        score_sell += 10

    if rb == "REJECTION":
        score_sell += 5

    if imb > 10:
        score_buy += 5
        score_sell += 5

    # decisão
    if score_buy > score_sell and score_buy > 30:
        direction = "BUY"
    elif score_sell > score_buy and score_sell > 30:
        direction = "SELL"
    else:
        direction = "NEUTRO"

    price = df["close"].iloc[-1]

    return {
        "direction": direction,
        "score_buy": score_buy,
        "score_sell": score_sell,
        "price": price
    }


# =========================
# 🔥 FINAL
# =========================
def analisar():
    if not connect():
        return {"erro": "Erro MT5"}

    mt5.symbol_select(SYMBOL, True)

    tfs = [
        mt5.TIMEFRAME_D1,
        mt5.TIMEFRAME_H1,
        mt5.TIMEFRAME_M15,
        mt5.TIMEFRAME_M5
    ]

    total_buy = 0
    total_sell = 0

    for tf in tfs:
        df = get_data(tf)
        if df is None:
            continue

        res = analyze_tf(df)

        total_buy += res["score_buy"]
        total_sell += res["score_sell"]

    if total_buy > total_sell:
        final = "BUY"
    elif total_sell > total_buy:
        final = "SELL"
    else:
        final = "NEUTRO"

    price = res["price"]

    return {
        "direcao": final,
        "entrada": round(price, 2),
        "stop": round(price - 15, 2),
        "tp": round(price + 30, 2),
        "modo": "INSTITUCIONAL V2"
        }
