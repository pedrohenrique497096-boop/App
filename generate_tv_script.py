def gerar_script(dados):

    script = f"""
//@version=5
indicator("Shark Institutional AI", overlay=true)

// 🔥 ZONAS
ob_buy = {dados['ob_compra']}
ob_sell = {dados['ob_venda']}
topo = {dados['topo']}
fundo = {dados['fundo']}

// 🔹 Desenhos
line.new(bar_index, ob_buy, bar_index+10, ob_buy, color=color.green, width=2)
line.new(bar_index, ob_sell, bar_index+10, ob_sell, color=color.red, width=2)

line.new(bar_index, topo, bar_index+10, topo, color=color.yellow)
line.new(bar_index, fundo, bar_index+10, fundo, color=color.orange)

// 🔥 Entrada
label.new(bar_index, close, "ENTRY", style=label.style_label_up)
"""

    with open("tv_script.pine", "w") as f:
        f.write(script)

    print("Script do TradingView gerado!")
