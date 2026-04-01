from PIL import Image
import numpy as np
import os

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        # caminho automático
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho = os.path.join(base_dir, "data", "Foto.jpg")

        print(f"Caminho usado: {caminho}")

        img = Image.open(caminho).convert("RGB")
        img_array = np.array(img)

        altura, largura, _ = img_array.shape
        print(f"Imagem carregada: {largura}x{altura}")

        # 🔥 CONVERTE PARA CINZA (estrutura)
        gray = np.mean(img_array, axis=2)

        # divide esquerda e direita
        meio = largura // 2
        esquerda = gray[:, :meio]
        direita = gray[:, meio:]

        media_esq = np.mean(esquerda)
        media_dir = np.mean(direita)

        # 🔥 LÓGICA DE TENDÊNCIA
        if media_dir > media_esq:
            direcao = "BUY"
            motivo = "Direita mais forte que esquerda (tendência de alta)"
        else:
            direcao = "SELL"
            motivo = "Direita mais fraca que esquerda (tendência de queda)"

        return {
            "direcao": direcao,
            "entrada": 0,
            "stop": 0,
            "tp": 0,
            "motivo": motivo
        }

    except Exception as e:
        return {
            "direcao": "NEUTRO",
            "entrada": 0,
            "stop": 0,
            "tp": 0,
            "motivo": f"Erro: {str(e)}"
        }
