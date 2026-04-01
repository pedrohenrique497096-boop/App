from vision.analyzer import analisar
from control.actions import executar
from visual.chart import desenhar

dados = analisar()
executar(dados)
desenhar(dados)
