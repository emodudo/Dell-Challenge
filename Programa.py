import pandas as pd
# Poder reiniciar o programa:
while True:
    distancia_df = pd.read_csv("distancia.csv", index_col=0)
# informações:
    taxas = {
        "pequeno": 4.87,
        "medio": 11.92,
        "grande": 27.44
    }

    pesos = {
        "celular": 0.5,
        "geladeira": 60.0,
        "freezer": 100.0,
        "cadeira": 5.0,
        "luminaria": 0.8,
        "lavadoura de roupa": 120.0
    }

    limites_carga = {
        "pequeno": 1.0,
        "medio": 4.0,
        "grande": 10.0
    }

    total_peso_produtos = 0.0

# Input de quantos produtos e cada tipo vão ser transportados + cálculo do peso total:
    produtos_na_parada = {}
    quantidades = [
        int(input(f"Quantos {produto}s serão carregados? ")) for produto in pesos]
    total_peso_produtos = sum([quantidade * peso_produto for quantidade,
                               peso_produto in zip(quantidades, pesos.values())])
# Input das cidades escolhidas para o transporte:
    peso = total_peso_produtos / 1000.0
    origem = input("Informe a cidade de partida: ").upper()
    parada = input(
        'Informe a cidade da parada intermediária (deixe em branco se não houver parada): ').upper()
    destino = input("Informe a cidade de destino: ").upper()
# Lista de combinações para cada tipo de transporte:
    if parada:
        origem_destinos = [(origem, destino),
                           (origem, parada), (parada, destino)]
    else:
        origem_destinos = [(origem, destino)]

    precos = []
    for origem_destino in origem_destinos:
        if origem_destino.count('') == 1:
            continue
# Mensagem de erro caso a cidade não esteja constando no arquivo csv:
        try:
            distancia = distancia_df.loc[origem_destino]
        except KeyError:
            print(
                f"Não foi possível encontrar a distância entre {origem_destino[0]} e {origem_destino[1]}")
            continue
# Escolha do caminhão adequado com base no peso dos produtos:
        distancia = distancia_df.loc[origem_destino]
        if peso <= limites_carga.get("pequeno", float('inf')):
            tipo_caminhao = "pequeno"
        elif peso <= limites_carga.get("medio", float('inf')):
            tipo_caminhao = "medio"
        else:
            tipo_caminhao = "grande"
        preco = distancia * taxas[tipo_caminhao]
        precos.append((preco, tipo_caminhao, distancia))
# Input de quantos produtos são descarregados na parada caso houver uma:
    if parada:
        produtos_parada = {}
        for produto in pesos:
            quantidade = int(
                input(f"Quantos {produto}s serão descarregados na parada? "))
            if quantidade > 0:
                produtos_parada[produto] = quantidade
# Retorno de quantos produtos foram descarregados na parada:
        if produtos_parada:
            print("Produtos descarregados na parada:")
            for produto, quantidade in produtos_parada.items():
                print(f"{quantidade} {produto}s")
        else:
            print("Nenhum produto será descarregado na parada.")
# Cálculo do peso e valor total do Transporte:
    preco_total = sum([preco for preco, _, _ in precos])
    print(f"O peso total da entrega é de {peso:.2f} toneladas")
    print(f"O preço do transporte é de R$ {preco_total:.2f}")
# Reiniciar ou não o programa:
    user_input = input("Deseja calcular novamente? (S/N)")
    if user_input.lower() == "n":
        break
