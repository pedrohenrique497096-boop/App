from vision.analyzer import analisar
from control.actions import executar
from visual.chart import desenhar

dados = analisar()

if "erro" in dados:
    print("Erro:", dados["erro"])
else:
    executar(dados)
    desenhar(dados)
