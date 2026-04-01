import matplotlib.pyplot as plt
import os

def desenhar(dados):
    try:
        x = list(range(50))
        y = [i + (i % 5) for i in x]

        plt.figure(figsize=(10,5))
        plt.plot(x, y)

        if dados["direcao"] != "NEUTRO":
            plt.axhline(dados["entrada"], linestyle="--", label="Entrada")
            plt.axhline(dados["stop"], color="red", label="Stop")
            plt.axhline(dados["tp"], color="green", label="TP")

        plt.legend()
        plt.title("Shark Black Institutional")

        caminho = os.path.join(os.getcwd(), "grafico_resultado.png")
        plt.savefig(caminho)

        print(f"\n📊 Gráfico salvo em: {caminho}")

        plt.close()

    except Exception as e:
        print("Erro ao desenhar gráfico:", e)
