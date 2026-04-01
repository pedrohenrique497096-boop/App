import matplotlib.pyplot as plt

def desenhar(dados):
    try:
        x = list(range(50))
        y = [i + (i % 5) for i in x]

        plt.figure()

        plt.plot(x, y)

        if dados["direcao"] != "NEUTRO":
            plt.axhline(dados["entrada"], linestyle="--", label="Entrada")
            plt.axhline(dados["stop"], color="red", label="Stop")
            plt.axhline(dados["tp"], color="green", label="TP")

        plt.legend()
        plt.title("IA Trading")

        plt.show()

    except Exception as e:
        print("Erro ao desenhar gráfico:", e)
