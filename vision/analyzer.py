import os

def analisar():

    modo = "mobile"  # 🔥 muda pra "mt5" no notebook

    if modo == "mt5":
        try:
            import MetaTrader5 as mt5
            import pandas as pd

            print("Modo MT5 (real)")

            if not mt5.initialize():
                return {"erro": "Erro ao conectar MT5"}

            symbol = "XAUUSD"
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)

            df = pd.DataFrame(rates)

            preco = df['close'].iloc[-1]
            high = df['high'].max()
            low = df['low'].min()

            direcao = "BUY"
            entrada = preco
            stop = low
            tp = entrada + (entrada - stop) * 2

            return {
                "direcao": direcao,
                "entrada": round(entrada, 2),
                "stop": round(stop, 2),
                "tp": round(tp, 2),
                "modo": "MT5 REAL"
            }

        except Exception as e:
            return {"erro": str(e)}

    else:
        # 🔥 MODO CELULAR (imagem)
        from PIL import Image
        import numpy as np

        print("Modo MOBILE (imagem)")

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho = os.path.join(base_dir, "data", "Foto.jpg")

            img = Image.open(caminho).convert("RGB")
            gray = np.mean(np.array(img), axis=2)

            preco = float(np.mean(gray))

            return {
                "direcao": "BUY",
                "entrada": round(preco, 2),
                "stop": round(preco - 10, 2),
                "tp": round(preco + 20, 2),
                "modo": "SIMULAÇÃO MOBILE"
            }

        except Exception as e:
            return {"erro": str(e)}
