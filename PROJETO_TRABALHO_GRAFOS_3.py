import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
from collections import defaultdict
from itertools import combinations

# Função para verificar se a atribuição de uma rodada para um jogo é válida
def verificar_atribuicao_valida(jogo, rodada_atual, grafo, contagem_rodadas, limite_jogos_por_rodada):
    # Parâmetro jogo é uma tupla(exemplo: 'CFC')
    # Parâmetro rodada_atual (dict): Atribuição atual de rodadas para os jogos,
    # Parâmetro grafo(networkx.Graph): Grafo que representa os jogos e suas restrições,
    # contagem_rodadas (dict): Contagem de jogos por rodada,
    # limite_jogos_por_rodada (int): Limite máximo de jogos por rodada
    # Retorna uma bool True se atribuição for válida, False o contrário
    
    rodada = rodada_atual[jogo]
    
    # Verificação das restrições de rodadas proibidas 
    '''
    Restrições de rodadas proibidas, limite de jogos por rodada e conflitos
    entre jogos que compartilham times ou têm restrições de mandante.

    '''
    restricoes = []
    if jogo in restricoes_rodadas:
        restricoes = restricoes_rodadas[jogo]
    elif (jogo[1], jogo[0]) in restricoes_rodadas:
        restricoes = restricoes_rodadas[(jogo[1], jogo[0])]
    if restricoes and int(rodada[1:]) in restricoes:
        return False

    # Verifica se a rodada atingiu o limite de jogos
    if contagem_rodadas[rodada] >= limite_jogos_por_rodada:
        return False

    # Verifica conflitos com jogos adjacentes
    for vizinho in grafo[jogo]:
        if vizinho in rodada_atual and rodada_atual[vizinho] == rodada:
            return False

    return True

#Função para atribuir rodadas aos jogos usando backtracking, respeitando as restrições.
def atribuir_rodadas(grafo, max_rodadas=14, limite_jogos_por_rodada=3):
# Parâmetro grafo(network.Graph): Grafo que representa os jogos e suas restrições conforme o modelo pdf pedido,
# Parâmetro max_rodadas (int): Número máximo de rodadas disponíveis,
# Parâmetro limite_jogos_por_rodada (int): Limite máximo de jogos por rodada.
# Retorna um dicionário que atribui as rodadas para os jogos ou None se não for possível.
    
    lista_jogos = [no for no in grafo if isinstance(no, tuple)]
    rodada_atual = {}
    contagem_rodadas = {f"R{i}": 0 for i in range(1, max_rodadas + 1)}

    def resolver_rodada(indice):
        if indice == len(lista_jogos):
            return True  # Todos os jogos foram atribuídos
        jogo = lista_jogos[indice]
        for rodada in contagem_rodadas:
            rodada_atual[jogo] = rodada
            if verificar_atribuicao_valida(jogo, rodada_atual, grafo, contagem_rodadas, limite_jogos_por_rodada):
                contagem_rodadas[rodada] += 1
                if resolver_rodada(indice + 1):
                    return True
                contagem_rodadas[rodada] -= 1  # Backtracking
            del rodada_atual[jogo]
        return False

    if resolver_rodada(0):
        return rodada_atual
    else:
        return None
    
# Função para desenhar o grafo com as rodadas atribuídas usando cores para representar as rodadas.
def desenhar_grafo(grafo, atribuicoes):
# Parâmetro grafo (networkx.Graph): Grafo que representa os jogos,
# Parâmetro atribuicoes (dict): Atribuição de rodadas para os jogos.
    fig, ax = plt.subplots(figsize=(12, 7))
    pos = nx.spring_layout(grafo, seed=42)

    # Normaliza as cores para as rodadas (1 a 14)
    norm = plt.Normalize(vmin=1, vmax=14)
    cores_nos = []
    for no in grafo.nodes():
        if no in atribuicoes:
            try:
                num_rodada = int(atribuicoes[no][1:])
                cores_nos.append(plt.cm.rainbow(norm(num_rodada)))
            except:
                cores_nos.append("gray")
        else:
            cores_nos.append("gray")
    
    # Desenha o grafo
    nx.draw_networkx_nodes(grafo, pos, node_color=cores_nos, ax=ax, node_size=800)
    nx.draw_networkx_edges(grafo, pos, ax=ax, edge_color="gray")
    
    # Rótulos dos nós
    rotulos = {no: f"{no[0]} X {no[1]}" for no in grafo.nodes()}
    nx.draw_networkx_labels(grafo, pos, labels=rotulos, ax=ax)
    
    # Legenda das rodadas
    legendas = []
    for r in range(1, 15):
        cor = plt.cm.rainbow(norm(r))
        patch = mpatches.Patch(color=cor, label=f"Rodada {r}")
        legendas.append(patch)
    ax.legend(handles=legendas, title="Rodadas", bbox_to_anchor=(1, 1))
    
    plt.title("Cronograma de Jogos por Rodada")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# Função que adiciona arestas ao grafo com base nas restrições de mandante e conflitos
def adicionar_restricoes_grafo(lista_jogos, restricoes_mandante, grafo):
# Parâmetro lista_jogos (list): Lista de todos os jogos possíveis;
# Parâmetro restricoes_mandante (dict): Restrições de mandante;
# Parâmetro grafo (networkx.Graph): Grafo onde as arestas serão adicionadas.
    
    for jogo1, jogo2 in combinations(lista_jogos, 2):
        # Conflito geral: times não podem jogar mais de uma vez na mesma rodada
        if jogo1[0] in jogo2 or jogo1[1] in jogo2:
            grafo.add_edge(jogo1, jogo2)

        # Conflito específico: restrições de mandante
        for (time1, time2), tipo in restricoes_mandante.items():
            if (jogo1[0] == time1 and jogo2[0] == time2) or (jogo1[0] == time2 and jogo2[0] == time1):
                grafo.add_edge(jogo1, jogo2)

# Função para exibir o cronograma de jogos organizado por rodada
def exibir_cronograma(cronograma):
# Parâmetro cronograma (dict) Dicionário com as rodadas e seus jogos.   
    
    for rodada, jogos in sorted(cronograma.items(), key=lambda x: int(x[0][1:])):
        print(f"!!!!Rodada {rodada[1:]}:!!!!")
        for (time1, time2) in jogos:
            print(f"{time1} X {time2}")
        print()

# Lista de times
times = ["DFC", "TFC", "AFC", "LFC", "FFC", "OFC", "CFC"]

# Gera todos os jogos possíveis (ida e volta)
jogos = [(t1, t2) for t1, t2 in combinations(times, 2)]
jogos += [(t2, t1) for t1, t2 in jogos]

# Cria o grafo
grafo = nx.Graph()
grafo.add_nodes_from(jogos)

# Restrições de mandante
restricoes_mandante = {
    ("TFC", "OFC"): "mandante",
    ("AFC", "FFC"): "mandante",
}

# Restrições de rodadas
restricoes_rodadas = {
    ("DFC", "CFC"): [1, 14],
    ("LFC", "FFC"): [7, 13],
    ("OFC", "LFC"): [10, 11],
    ("AFC", "FFC"): [12, 13],
    ("CFC", "TFC"): [2, 3]
}

# Adiciona restrições ao grafo
adicionar_restricoes_grafo(jogos, restricoes_mandante, grafo)

# Atribui rodadas aos jogos
atribuicoes = atribuir_rodadas(grafo)

# Organiza o cronograma
cronograma = defaultdict(list)
for jogo, rodada in atribuicoes.items():
    cronograma[rodada].append(jogo)
exibir_cronograma(cronograma)

# Plota o grafo
desenhar_grafo(grafo, atribuicoes)