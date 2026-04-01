import cv2

def analisar():
    print("Analisando imagem do gráfico...")

    try:
        img = cv2.imread("data/grafico.png")

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

    except:
        return {
            "direcao": "NEUTRO",
            "entrada": 0,
            "stop": 0,
            "tp": 0,
            "motivo": "Erro ao ler imagem"
        }
