import cv2

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        # CAMINHO DIRETO NO CELULAR
        caminho = "/storage/emulated/0/ia-trading-vision/data/grafico.png"

        img = cv2.imread(caminho)

        if img is None:
            raise Exception("Imagem não encontrada")

        altura, largura, _ = img.shape

        print(f"Imagem carregada: {largura}x{altura}")

        # análise simples (base)
        media_cor = img.mean()

        if media_cor > 100:
            direcao = "BUY"
            motivo = "Imagem clara (simulação de alta)"
        else:
            direcao = "SELL"
            motivo = "Imagem escura (simulação de queda)"

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
