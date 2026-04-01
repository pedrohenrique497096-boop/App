from PIL import Image
import numpy as np
import os

def analisar():
    print("Analisando com lógica institucional completa...")

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho = os.path.join(base_dir, "data", "Foto.jpg")

        img = Image.open(caminho).convert("RGB")
        img_array = np.array(img)

        altura, largura, _ = img_array.shape
        print(f"Imagem carregada: {largura}x{altura}")

        # ===============================
        # 🔹 CONVERTER PARA ESCALA CINZA
        # ===============================
        gray = np.mean(img_array, axis=2)

        # ===============================
        # 🔹 DIVIDIR EM PARTES (AMD)
        # ===============================
        terco = largura // 3
        esquerda = gray[:, :terco]
        meio = gray[:, terco:2*terco]
        direita = gray[:, 2*terco:]

        media_esq = np.mean(esquerda)
        media_meio = np.mean(meio)
        media_dir = np.mean(direita)

        # ===============================
        # 🔹 AMD (Manipulação)
        # ===============================
        manipulacao = media_meio < media_esq and media_meio < media_dir

        # ===============================
        # 🔹 LIQUIDEZ (simplificado)
        # ===============================
        topo = np.min(gray)
        fundo = np.max(gray)

        sweep = abs(media_esq - media_dir) > 5

        # ===============================
        # 🔹 BOS / CHOCH (estrutura)
        # ===============================
        if media_dir > media_esq:
            estrutura = "BOS_ALTA"
        elif media_dir < media_esq:
            estrutura = "BOS_BAIXA"
        else:
            estrutura = "LATERAL"

        # ===============================
        # 🔹 EQUAL HIGH / LOW (simples)
        # ===============================
        equal_zone = abs(topo - fundo) < 2

        # ===============================
        # 🔹 FVG / IMBALANCE (simples)
        # ===============================
        desequilibrio = abs(media_esq - media_dir) > 10

        # ===============================
        # 🔹 DECISÃO FINAL (SMC)
        # ===============================
        if manipulacao and estrutura == "BOS_ALTA" and desequilibrio:
            direcao = "BUY"
            motivo = "AMD + BOS Alta + Imbalance"
        elif manipulacao and estrutura == "BOS_BAIXA" and desequilibrio:
            direcao = "SELL"
            motivo = "AMD + BOS Baixa + Imbalance"
        elif sweep and estrutura == "BOS_ALTA":
            direcao = "BUY"
            motivo = "Liquidity Sweep + Continuação"
        elif sweep and estrutura == "BOS_BAIXA":
            direcao = "SELL"
            motivo = "Liquidity Sweep + Queda"
        else:
            direcao = "NEUTRO"
            motivo = "Sem confluência institucional"

        return {
            "direcao": direcao,
            "entrada": 0,
            "stop": 0,
            "tp": 0,
            "motivo": motivo,
            "estrutura": estrutura,
            "manipulacao": manipulacao,
            "liquidez": sweep,
            "imbalance": desequilibrio
        }

    except Exception as e:
        return {
            "direcao": "NEUTRO",
            "entrada": 0,
            "stop": 0,
            "tp": 0,
            "motivo": f"Erro: {str(e)}"
    }
