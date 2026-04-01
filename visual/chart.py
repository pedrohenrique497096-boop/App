import matplotlib.pyplot as plt

def desenhar(dados):

    plt.figure(figsize=(10,5))

    # simulação de gráfico
    x = list(range(50))
    y = [i + (i%5)*2 for i in x]

    plt.plot(x, y)

    # 🔥 DESENHOS DA IA
    if dados["direcao"] != "NEUTRO":

        plt.axhline(dados["entrada"], linestyle="--", label="Entrada")
        plt.axhline(dados["stop"], linestyle="--", color="red", label="Stop")
        plt.axhline(dados["tp"], linestyle="--", color="green", label="TP")

        plt.axhline(dados["ob_compra"], linestyle=":", color="green", label="OB Compra")
        plt.axhline(dados["ob_venda"], linestyle=":", color="red", label="OB Venda")

    plt.legend()
    plt.title("Shark Black Institutional")

    plt.show()
