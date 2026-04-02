import streamlit as st
from vision.analyzer import analisar
from control.actions import executar
from visual.chart import desenhar
import os

st.set_page_config(layout="wide")

st.title("🔥 Shark Black Institutional")

if st.button("Analisar XAUUSD"):

    dados = analisar()

    if "erro" in dados:
        st.error(dados["erro"])

    else:
        # 🔥 EXECUTA DECISÃO (actions.py)
        executar(dados)

        # 🔥 GERA GRÁFICO (chart.py)
        desenhar(dados)

        # 🔥 MOSTRAR NO APP
        if dados["direcao"] == "BUY":
            st.success(f"Direção: {dados['direcao']}")
        elif dados["direcao"] == "SELL":
            st.error(f"Direção: {dados['direcao']}")
        else:
            st.warning("Sem entrada")

        col1, col2, col3 = st.columns(3)

        col1.metric("Entrada", dados["entrada"])
        col2.metric("Stop", dados["stop"])
        col3.metric("TP", dados["tp"])

        st.write("### Estrutura:", dados["estrutura"])
        st.write("Liquidez:", dados["liquidez"])
        st.write("Imbalance:", dados["imbalance"])
        st.write("Motivo:", dados["motivo"])

        # 🔥 MOSTRAR GRÁFICO GERADO
        caminho = os.path.join(os.getcwd(), "grafico_resultado.png")

        if os.path.exists(caminho):
            st.image(caminho)
