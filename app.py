import streamlit as st
from vision.analyzer import analisar

st.set_page_config(layout="wide", page_title="Shark Black Institutional")

st.title("🔥 Shark Black Institutional")
st.caption("XAUUSD multi-timeframe institucional")

if st.button("Analisar XAUUSD"):
    dados = analisar()

    if "erro" in dados:
        st.error(dados["erro"])
    else:
        final_direction = dados["final_direction"]

        if final_direction == "BUY":
            st.success(f"Direção final: {final_direction}")
        elif final_direction == "SELL":
            st.error(f"Direção final: {final_direction}")
        else:
            st.warning("Direção final: NEUTRO")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Ativo", dados["symbol"])
        col2.metric("Candles", dados["candles_used"])
        col3.metric("Score BUY", dados["weighted_buy"])
        col4.metric("Score SELL", dados["weighted_sell"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Entrada", dados["entrada"])
        c2.metric("Stop", dados["stop"])
        c3.metric("TP", dados["tp"])

        st.write("### Motivo principal")
        st.write(dados["motivo"])

        st.write("## Análises por timeframe")

        for tf, info in dados["timeframes"].items():
            with st.expander(f"{tf} | {info['direction']} | Score {info['score']}", expanded=(tf == "M5")):
                a, b, c = st.columns(3)
                a.metric("Close", info["close"])
                b.metric("Trend", info["trend"])
                c.metric("Direção", info["direction"])

                d, e, f = st.columns(3)
                d.metric("Entrada", info["entrada"])
                e.metric("Stop", info["stop"])
                f.metric("TP", info["tp"])

                g, h, i = st.columns(3)
                g.metric("BOS", info["bos"])
                h.metric("CHoCH", info["choch"])
                i.metric("Sweep", info["sweep"])

                j, k, l = st.columns(3)
                j.metric("EQH", info["eqh"] if info["eqh"] is not None else "-")
                k.metric("EQL", info["eql"] if info["eql"] is not None else "-")
                l.metric("AMD", info["amd"])

                m, n, o = st.columns(3)
                m.metric("PDH", info["pdh"] if info["pdh"] is not None else "-")
                n.metric("PDL", info["pdl"] if info["pdl"] is not None else "-")
                o.metric("FVG", info["fvg_type"])

                p, q, r = st.columns(3)
                p.metric("OB", info["ob_type"])
                q.metric("OB Top", info["ob_top"] if info["ob_top"] is not None else "-")
                r.metric("OB Bottom", info["ob_bottom"] if info["ob_bottom"] is not None else "-")

                st.write("**Motivo:**", info["motivo"])
