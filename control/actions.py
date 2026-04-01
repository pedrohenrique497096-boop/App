def executar(dados):
    print("\n===== DECISÃO DA IA =====")
    print(f"Direção: {dados['direcao']}")
    print(f"Estrutura: {dados.get('estrutura')}")
    print(f"Manipulação: {dados.get('manipulacao')}")
    print(f"Liquidez: {dados.get('liquidez')}")
    print(f"Imbalance: {dados.get('imbalance')}")
    print(f"Motivo: {dados['motivo']}")
