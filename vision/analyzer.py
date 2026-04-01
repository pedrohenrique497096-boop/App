from PIL import Image
import numpy as np

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        # CAMINHO CORRETO DO SEU PROJETO
        caminho = "/storage/emulated/0/Download/App-main (4)/App-main/data/grafico.png"

        img = Image.open(caminho)
        img_array = np.array(img)

        altura, largura, _ = img_array.shape

        print(f"Imagem carregada: {largura}x{altura}")

        # análise simples (base)
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
