import MetaTrader5 as mt5
import pandas as pd
import numpy as np

SYMBOL = "XAUUSDm"
CANDLE_LIMIT = 1000

TIMEFRAMES = {
    "D1": mt5.TIMEFRAME_D1,
    "H4": mt5.TIMEFRAME_H4,
    "H1": mt5.TIMEFRAME_H1,
    "M15": mt5.TIMEFRAME_M15,
    "M5": mt5.TIMEFRAME_M5,
}

TF_WEIGHTS = {
    "D1": 5,
    "H4": 4,
    "H1": 3,
    "M15": 2,
    "M5": 1,
}


def _connect():
    paths = [
        "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "C:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe",
    ]

    for path in paths:
        if mt5.initialize(path=path):
            return True

    return mt5.initialize()


def _get_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df


def _swings(df, left=2, right=2):
    highs = []
    lows = []

    for i in range(left, len(df) - right):
        h = df["high"].iloc[i]
        l = df["low"].iloc[i]

        if h == df["high"].iloc[i-left:i+right+1].max():
            highs.append((i, h))

        if l == df["low"].iloc[i-left:i+right+1].min():
            lows.append((i, l))

    return highs, lows


def _last_two(values):
    if len(values) >= 2:
        return values[-2], values[-1]
    elif len(values) == 1:
        return values[0], values[0]
    return None, None


def _detect_structure(df):
    highs, lows = _swings(df)

    prev_high, last_high = _last_two(highs)
    prev_low, last_low = _last_two(lows)

    close_now = df["close"].iloc[-1]

    bos = "NONE"
    choch = "NONE"
    trend = "RANGE"

    if last_high and close_now > last_high[1]:
        bos = "BOS_ALTA"
    elif last_low and close_now < last_low[1]:
        bos = "BOS_BAIXA"

    if prev_high and last_high and prev_low and last_low:
        hh = last_high[1] > prev_high[1]
        hl = last_low[1] > prev_low[1]
        lh = last_high[1] < prev_high[1]
        ll = last_low[1] < prev_low[1]

        if hh and hl:
            trend = "ALTA"
        elif lh and ll:
            trend = "BAIXA"

        # CHoCH simples: quebra contra a estrutura anterior
        if trend == "ALTA" and close_now < last_low[1]:
            choch = "CHOCH_BAIXA"
        elif trend == "BAIXA" and close_now > last_high[1]:
            choch = "CHOCH_ALTA"

    return {
        "trend": trend,
        "bos": bos,
        "choch": choch,
        "swing_highs": highs,
        "swing_lows": lows,
    }


def _detect_equal_levels(df, tolerance=0.8):
    highs, lows = _swings(df)

    _, last_high = _last_two(highs)
    _, last_low = _last_two(lows)

    eqh = None
    eql = None

    if len(highs) >= 2:
        h1 = highs[-1][1]
        h2 = highs[-2][1]
        if abs(h1 - h2) <= tolerance:
            eqh = round((h1 + h2) / 2, 2)

    if len(lows) >= 2:
        l1 = lows[-1][1]
        l2 = lows[-2][1]
        if abs(l1 - l2) <= tolerance:
            eql = round((l1 + l2) / 2, 2)

    return eqh, eql


def _detect_liquidity_sweep(df, eqh, eql):
    last = df.iloc[-1]
    sweep = "NONE"

    if eqh is not None:
        if last["high"] > eqh and last["close"] < eqh:
            sweep = "BUY_SIDE_LIQUIDITY_SWEEP"

    if eql is not None:
        if last["low"] < eql and last["close"] > eql:
            sweep = "SELL_SIDE_LIQUIDITY_SWEEP"

    return sweep


def _detect_pdh_pdl(d1_df):
    if len(d1_df) < 2:
        return None, None
    prev_day = d1_df.iloc[-2]
    return round(prev_day["high"], 2), round(prev_day["low"], 2)


def _detect_fvg(df):
    if len(df) < 4:
        return {"type": "NONE", "top": None, "bottom": None, "size": 0}

    c1 = df.iloc[-3]
    c3 = df.iloc[-1]

    # bullish FVG
    if c3["low"] > c1["high"]:
        return {
            "type": "BULLISH_FVG",
            "top": round(c3["low"], 2),
            "bottom": round(c1["high"], 2),
            "size": round(c3["low"] - c1["high"], 2)
        }

    # bearish FVG
    if c3["high"] < c1["low"]:
        return {
            "type": "BEARISH_FVG",
            "top": round(c1["low"], 2),
            "bottom": round(c3["high"], 2),
            "size": round(c1["low"] - c3["high"], 2)
        }

    return {"type": "NONE", "top": None, "bottom": None, "size": 0}


def _detect_order_block(df):
    if len(df) < 20:
        return {"type": "NONE", "top": None, "bottom": None}

    recent = df.tail(20).copy()
    recent["body"] = (recent["close"] - recent["open"]).abs()
    avg_body = recent["body"].mean()

    # última vela oposta antes do impulso
    for i in range(len(recent) - 3, 2, -1):
        curr = recent.iloc[i]
        nxt = recent.iloc[i + 1]

        # bullish displacement after bearish candle
        if curr["close"] < curr["open"] and (nxt["close"] - nxt["open"]) > avg_body * 1.5:
            return {
                "type": "BULLISH_OB",
                "top": round(curr["high"], 2),
                "bottom": round(curr["low"], 2)
            }

        # bearish displacement after bullish candle
        if curr["close"] > curr["open"] and (nxt["open"] - nxt["close"]) > avg_body * 1.5:
            return {
                "type": "BEARISH_OB",
                "top": round(curr["high"], 2),
                "bottom": round(curr["low"], 2)
            }

    return {"type": "NONE", "top": None, "bottom": None}


def _detect_amd(df):
    if len(df) < 30:
        return {"phase": "NONE", "model": "NONE"}

    part = df.tail(30)
    thirds = np.array_split(part, 3)

    r1 = thirds[0]["high"].max() - thirds[0]["low"].min()
    r2 = thirds[1]["high"].max() - thirds[1]["low"].min()
    r3 = thirds[2]["high"].max() - thirds[2]["low"].min()

    c1 = thirds[0]["close"].iloc[-1]
    c2 = thirds[1]["close"].iloc[-1]
    c3 = thirds[2]["close"].iloc[-1]

    if r2 < r1 and r3 > r2:
        if c3 > c2:
            return {"phase": "DISTRIBUTION_UP", "model": "AMD_BULLISH"}
        if c3 < c2:
            return {"phase": "DISTRIBUTION_DOWN", "model": "AMD_BEARISH"}

    return {"phase": "MIXED", "model": "NONE"}


def _score_analysis(close_now, structure, eqh, eql, sweep, fvg, ob, amd, pdh, pdl):
    score_buy = 0
    score_sell = 0
    reasons_buy = []
    reasons_sell = []

    if structure["trend"] == "ALTA":
        score_buy += 20
        reasons_buy.append("Trend alta")

    if structure["trend"] == "BAIXA":
        score_sell += 20
        reasons_sell.append("Trend baixa")

    if structure["bos"] == "BOS_ALTA":
        score_buy += 20
        reasons_buy.append("BOS alta")

    if structure["bos"] == "BOS_BAIXA":
        score_sell += 20
        reasons_sell.append("BOS baixa")

    if structure["choch"] == "CHOCH_ALTA":
        score_buy += 12
        reasons_buy.append("CHoCH alta")

    if structure["choch"] == "CHOCH_BAIXA":
        score_sell += 12
        reasons_sell.append("CHoCH baixa")

    if sweep == "SELL_SIDE_LIQUIDITY_SWEEP":
        score_buy += 15
        reasons_buy.append("Sweep sell-side")

    if sweep == "BUY_SIDE_LIQUIDITY_SWEEP":
        score_sell += 15
        reasons_sell.append("Sweep buy-side")

    if fvg["type"] == "BULLISH_FVG":
        score_buy += 10
        reasons_buy.append("Bullish FVG")

    if fvg["type"] == "BEARISH_FVG":
        score_sell += 10
        reasons_sell.append("Bearish FVG")

    if ob["type"] == "BULLISH_OB":
        score_buy += 10
        reasons_buy.append("Bullish OB")

    if ob["type"] == "BEARISH_OB":
        score_sell += 10
        reasons_sell.append("Bearish OB")

    if amd["model"] == "AMD_BULLISH":
        score_buy += 8
        reasons_buy.append("AMD bullish")

    if amd["model"] == "AMD_BEARISH":
        score_sell += 8
        reasons_sell.append("AMD bearish")

    if pdh is not None and close_now > pdh:
        score_buy += 5
        reasons_buy.append("Acima do PDH")

    if pdl is not None and close_now < pdl:
        score_sell += 5
        reasons_sell.append("Abaixo do PDL")

    if eqh is not None:
        reasons_sell.append("EQH presente")
    if eql is not None:
        reasons_buy.append("EQL presente")

    return score_buy, score_sell, reasons_buy, reasons_sell


def _build_trade(close_now, direction, ob, recent_high, recent_low):
    if direction == "BUY":
        stop = ob["bottom"] if ob["type"] == "BULLISH_OB" and ob["bottom"] is not None else recent_low
        risk = max(close_now - stop, 0.5)
        tp = close_now + (risk * 2)
        return round(close_now, 2), round(stop, 2), round(tp, 2)

    if direction == "SELL":
        stop = ob["top"] if ob["type"] == "BEARISH_OB" and ob["top"] is not None else recent_high
        risk = max(stop - close_now, 0.5)
        tp = close_now - (risk * 2)
        return round(close_now, 2), round(stop, 2), round(tp, 2)

    return 0, 0, 0


def _analyze_timeframe(tf_name, tf_value, d1_df):
    df = _get_rates(SYMBOL, tf_value, CANDLE_LIMIT)
    if df is None or len(df) < 50:
        return None

    close_now = float(df["close"].iloc[-1])
    recent_high = float(df["high"].tail(20).max())
    recent_low = float(df["low"].tail(20).min())

    structure = _detect_structure(df)
    eqh, eql = _detect_equal_levels(df)
    sweep = _detect_liquidity_sweep(df, eqh, eql)
    fvg = _detect_fvg(df)
    ob = _detect_order_block(df)
    amd = _detect_amd(df)
    pdh, pdl = _detect_pdh_pdl(d1_df)

    score_buy, score_sell, reasons_buy, reasons_sell = _score_analysis(
        close_now, structure, eqh, eql, sweep, fvg, ob, amd, pdh, pdl
    )

    if score_buy > score_sell and score_buy >= 35:
        direction = "BUY"
        reasons = reasons_buy
        score = score_buy
    elif score_sell > score_buy and score_sell >= 35:
        direction = "SELL"
        reasons = reasons_sell
        score = score_sell
    else:
        direction = "NEUTRO"
        reasons = ["Sem confluência forte"]
        score = max(score_buy, score_sell)

    entrada, stop, tp = _build_trade(close_now, direction, ob, recent_high, recent_low)

    return {
        "timeframe": tf_name,
        "close": round(close_now, 2),
        "trend": structure["trend"],
        "bos": structure["bos"],
        "choch": structure["choch"],
        "eqh": eqh,
        "eql": eql,
        "sweep": sweep,
        "pdh": pdh,
        "pdl": pdl,
        "fvg_type": fvg["type"],
        "fvg_top": fvg["top"],
        "fvg_bottom": fvg["bottom"],
        "ob_type": ob["type"],
        "ob_top": ob["top"],
        "ob_bottom": ob["bottom"],
        "amd": amd["model"],
        "direction": direction,
        "score": int(score),
        "entrada": entrada,
        "stop": stop,
        "tp": tp,
        "motivo": " | ".join(reasons[:5]),
    }


def analisar():
    if not _connect():
        return {"erro": "Erro ao conectar MT5"}

    if not mt5.symbol_select(SYMBOL, True):
        return {"erro": f"Erro ao selecionar {SYMBOL}"}

    d1_df = _get_rates(SYMBOL, mt5.TIMEFRAME_D1, CANDLE_LIMIT)
    if d1_df is None or len(d1_df) == 0:
        return {"erro": "Sem dados D1"}

    analyses = {}

    for tf_name, tf_value in TIMEFRAMES.items():
        result = _analyze_timeframe(tf_name, tf_value, d1_df)
        if result:
            analyses[tf_name] = result

    if not analyses:
        return {"erro": "Sem análises disponíveis"}

    weighted_buy = 0
    weighted_sell = 0

    for tf, data in analyses.items():
        w = TF_WEIGHTS[tf]
        if data["direction"] == "BUY":
            weighted_buy += data["score"] * w
        elif data["direction"] == "SELL":
            weighted_sell += data["score"] * w

    if weighted_buy > weighted_sell and weighted_buy >= 250:
        final_direction = "BUY"
    elif weighted_sell > weighted_buy and weighted_sell >= 250:
        final_direction = "SELL"
    else:
        final_direction = "NEUTRO"

    # entrada final = prioriza M5, depois M15
    entry_tf = analyses.get("M5") or analyses.get("M15") or list(analyses.values())[-1]

    return {
        "modo": "SMC MTF PRO",
        "symbol": SYMBOL,
        "candles_used": CANDLE_LIMIT,
        "final_direction": final_direction,
        "weighted_buy": int(weighted_buy),
        "weighted_sell": int(weighted_sell),
        "entrada": entry_tf["entrada"] if final_direction != "NEUTRO" else 0,
        "stop": entry_tf["stop"] if final_direction != "NEUTRO" else 0,
        "tp": entry_tf["tp"] if final_direction != "NEUTRO" else 0,
        "motivo": entry_tf["motivo"],
        "timeframes": analyses,
        }
