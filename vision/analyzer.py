from PIL import Image
import numpy as np
import os

def analisar():
    print("Analisando com IA institucional PRO...")

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho = os.path.join(base_dir, "data", "Foto.jpg")

        img = Image.open(caminho).convert("RGB")
        img_array = np.array(img)

        gray = np.mean(img_array, axis=2)
        altura, largura = gray.shape

        esquerda = gray[:, :largura//2]
        direita = gray[:, largura//2:]

        media_esq = np.mean(esquerda)
        media_dir = np.mean(direita)

        # 🔹 Estrutura
        if media_dir > media_esq:
            estrutura = "ALTA"
        else:
            estrutura = "BAIXA"

        # 🔹 Liquidez
        topo = np.min(gray)
        fundo = np.max(gray)

        # 🔹 OB (zona institucional simulada)
        ob_compra = fundo + (fundo * 0.01)
        ob_venda = topo - (topo * 0.01)

        # 🔹 FVG (gap)
        fvg = abs(media_dir - media_esq)

        preco = np.mean(gray)

        # 🔥 DECISÃO
        if estrutura == "ALTA" and preco <= ob_compra:
            direcao = "BUY"
            entrada = preco
            stop = fundo
            tp = entrada + (entrada - stop) * 2
            motivo = "OB + tendência de alta"

        elif estrutura == "BAIXA" and preco >= ob_venda:
            direcao = "SELL"
            entrada = preco
            stop = topo
            tp = entrada - (stop - entrada) * 2
            motivo = "OB + tendência de baixa"

        else:
            direcao = "NEUTRO"
            entrada = stop = tp = 0
            motivo = "Sem entrada"

        return {
            "direcao": direcao,
            "entrada": round(entrada, 2),
            "stop": round(stop, 2),
            "tp": round(tp, 2),
            "ob_compra": round(ob_compra, 2),
            "ob_venda": round(ob_venda, 2),
            "topo": round(topo, 2),
            "fundo": round(fundo, 2),
            "motivo": motivo
        }

    except Exception as e:
        return {"erro": str(e)}
