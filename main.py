from vision.analyzer import analisar
from control.actions import executar
from generate_tv_script import gerar_script

dados = analisar()
executar(dados)

if dados.get("direcao") != "NEUTRO":
    gerar_script(dados)
