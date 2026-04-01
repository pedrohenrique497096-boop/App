from PIL import Image
import numpy as np
import os

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        # pega o caminho automaticamente
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho = os.path.join(base_dir, "data", "Foto.jpg")

        print(f"Caminho usado: {caminho}")

        img = Image.open(caminho)
        img = img.convert("RGB")
        img_array = np.array(img)

        altura, largura, _ = img_array.shape

        print(f"Imagem carregada: {largura}x{altura}")

        media_cor = img_array.mean()

        if media_cor > 120:
            direcao = "BUY"
            motivo = "Imagem clara (possível alta)"
        else:
            direcao = "SELL"
            motivo = "Imagem escura (possível queda)"

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
