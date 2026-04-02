import os

def analisar():

    modo = "mt5"  # 🔥 AGORA É REAL

    if modo == "mt5":
        try:
            import MetaTrader5 as mt5
            import pandas as pd

            print("Modo MT5 (real)")

            if not mt5.initialize():
                return {"erro": "Erro ao conectar MT5"}

            symbol = "XAUUSDm"  # 🔥 CORRETO
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)

            if rates is None or len(rates) == 0:
                return {"erro": "Sem dados do MT5"}

            df = pd.DataFrame(rates)

            preco = df['close'].iloc[-1]
            high = df['high'].max()
            low = df['low'].min()

            # 🔥 ESTRUTURA
            if df['close'].iloc[-1] > df['close'].iloc[-20]:
                estrutura = "ALTA"
            else:
                estrutura = "BAIXA"

            # 🔥 LIQUIDEZ
            liquidez = abs(high - low)

            # 🔥 IMBALANCE (força)
            imbalance = abs(df['close'].iloc[-1] - df['open'].iloc[-1])

            # 🔥 DECISÃO
            if estrutura == "ALTA" and imbalance > 0.2:
                direcao = "BUY"
                entrada = preco
                stop = low
                tp = entrada + (entrada - stop) * 2
                motivo = "Tendência + força"

            elif estrutura == "BAIXA" and imbalance > 0.2:
                direcao = "SELL"
                entrada = preco
                stop = high
                tp = entrada - (stop - entrada) * 2
                motivo = "Queda + força"

            else:
                direcao = "NEUTRO"
                entrada = stop = tp = 0
                motivo = "Sem força"

            return {
                "direcao": direcao,
                "entrada": round(entrada, 2),
                "stop": round(stop, 2),
                "tp": round(tp, 2),
                "estrutura": estrutura,
                "liquidez": round(liquidez, 2),
                "imbalance": round(imbalance, 2),
                "motivo": motivo,
                "modo": "MT5 REAL"
            }

        except Exception as e:
            return {"erro": str(e)}

    else:
        return {"erro": "Modo inválido"}
