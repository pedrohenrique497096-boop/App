import streamlit as st
from vision.analyzer import analisar

st.set_page_config(layout="wide")

st.title("🔥 Shark Black Institutional")

if st.button("Analisar XAUUSD"):

    dados = analisar()

    if "erro" in dados:
        st.error(dados["erro"])
    else:
        st.success(f"Direção: {dados['direcao']}")

        st.write("### Estrutura:", dados["estrutura"])
        st.write("Entrada:", dados["entrada"])
        st.write("Stop:", dados["stop"])
        st.write("TP:", dados["tp"])
        st.write("Motivo:", dados["motivo"])
