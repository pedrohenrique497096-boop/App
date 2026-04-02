import matplotlib.pyplot as plt
import os

def desenhar(dados):

    x = list(range(100))
    y = [i + (i % 7) for i in x]

    plt.figure(figsize=(12,6))
    plt.plot(x, y)

    if dados["direcao"] != "NEUTRO":
        plt.axhline(dados["entrada"], linestyle="--", label="Entrada")
        plt.axhline(dados["stop"], linestyle="--", label="Stop")
        plt.axhline(dados["tp"], linestyle="--", label="TP")

    plt.title("Shark Black Institutional AI")
    plt.legend()

    caminho = os.path.join(os.getcwd(), "grafico_resultado.png")
    plt.savefig(caminho)

    print(f"\n📊 Gráfico salvo em: {caminho}")
