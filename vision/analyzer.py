from PIL import Image
import numpy as np

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        # AGORA USANDO Foto.jpg
        caminho = "/storage/emulated/0/Download/App-main (4)/App-main/data/Foto.jpg"

        img = Image.open(caminho)
        img = img.convert("RGB")  # garante formato correto
        img_array = np.array(img)

        altura, largura, _ = img_array.shape

        print(f"Imagem carregada: {largura}x{altura}")

        # análise simples
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
