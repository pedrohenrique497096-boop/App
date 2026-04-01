import os

def analisar():

    modo = "mobile"  # 🔥 depois no notebook muda pra "mt5"

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
                "estrutura": "REAL",
                "liquidez": round(high - low, 2),
                "imbalance": 0,
                "motivo": "Dados reais MT5",
                "modo": "MT5 REAL"
            }

        except Exception as e:
            return {"erro": str(e)}

    else:
        # 🔥 MODO MOBILE PRO
        from PIL import Image
        import numpy as np

        print("Modo MOBILE PRO (imagem)")

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho = os.path.join(base_dir, "data", "Foto.jpg")

            img = Image.open(caminho).convert("RGB")
            gray = np.mean(np.array(img), axis=2)

            altura, largura = gray.shape

            esquerda = gray[:, :largura//2]
            direita = gray[:, largura//2:]

            media_esq = np.mean(esquerda)
            media_dir = np.mean(direita)

            # 🔥 ESTRUTURA
            if media_dir > media_esq:
                estrutura = "ALTA"
            else:
                estrutura = "BAIXA"

            # 🔥 LIQUIDEZ
            topo = float(np.min(gray))
            fundo = float(np.max(gray))
            liquidez = abs(topo - fundo)

            # 🔥 IMBALANCE
            imbalance = abs(media_dir - media_esq)

            preco = float(np.mean(gray))

            # 🔥 DECISÃO
            if estrutura == "ALTA" and imbalance > 2:
                direcao = "BUY"
                entrada = preco
                stop = preco - 10
                tp = preco + 20
                motivo = "Tendência + força"

            elif estrutura == "BAIXA" and imbalance > 2:
                direcao = "SELL"
                entrada = preco
                stop = preco + 10
                tp = preco - 20
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
                "modo": "MOBILE PRO"
            }

        except Exception as e:
            return {"erro": str(e)}
