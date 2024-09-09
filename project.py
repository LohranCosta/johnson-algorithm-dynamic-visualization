import networkx as nx
import matplotlib.pyplot as plt
import time

# Função para desenhar o grafo e destacar uma aresta se necessário
def draw_graph_dynamic(G, pos, edge_to_highlight=None, title="Mostragem do Grafo"):
    plt.clf()  # Limpa a tela do gráfico
    plt.title(title)
    
    # Desenha o grafo com nós e arestas
    nx.draw(G, pos, with_labels=True, node_color='black', node_size=500, 
            font_size=10, font_weight='bold', font_color='white')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Se precisar destacar uma aresta, faz isso em vermelho
    if edge_to_highlight:
        nx.draw_networkx_edges(G, pos, edgelist=edge_to_highlight, edge_color='red', width=2.5)
    
    plt.pause(3)  # Espera 3 segundos para mostrar cada passo

# Função para converter um caminho de nós em uma lista de arestas
def path_to_edges(path):
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]

# Função principal que executa o Algoritmo de Johnson com visualização
def johnson_algorithm_visual(G):
    # Passo 1: Adiciona um vértice fictício "s" com arestas de peso 0 para todos os outros vértices
    s = 's'
    G.add_node(s)
    for v in list(G.nodes):
        if v != s:
            G.add_edge(s, v, weight=0)
    
    # Mostra o grafo com o vértice fictício
    pos = nx.spring_layout(G)
    draw_graph_dynamic(G, pos, title="Grafo Original com Vértice Fictício 's'")
    
    # Passo 2: Executa Bellman-Ford a partir do vértice fictício
    try:
        h = nx.single_source_bellman_ford_path_length(G, s)
    except nx.NetworkXUnbounded:
        print("Ciclo negativo encontrado!")
        return None
    
    # Remove o vértice fictício
    G.remove_node(s)
    
    # Atualiza os pesos das arestas usando os valores calculados
    reweighted_edges = []
    for u, v, w in G.edges(data='weight'):
        new_weight = w + h[u] - h[v]
        reweighted_edges.append((u, v, new_weight))
    G.add_weighted_edges_from(reweighted_edges)
    
    # Mostra o grafo com os pesos atualizados
    draw_graph_dynamic(G, pos, title="Grafo com Arestas Reponderadas")
    
    # Passo 3: Executa Dijkstra para cada vértice
    distances = {}
    paths = {}
    for u in G.nodes:
        distances[u] = {}
        paths[u] = {}
        for v in G.nodes:
            if u != v:
                # Encontra o caminho mais curto de u para v
                path = nx.shortest_path(G, source=u, target=v, weight='weight')
                path_edges = path_to_edges(path)
                paths[u][v] = path  # Salva o caminho mínimo
                
                # Destaca cada aresta do caminho para visualização
                for edge in path_edges:
                    draw_graph_dynamic(G, pos, edge_to_highlight=[edge], title=f"Verificando Caminho {u} -> {v}")
                
                # Calcula a distância mínima
                distances[u][v] = nx.shortest_path_length(G, source=u, target=v, weight='weight')
    
    # Ajusta as distâncias reais usando o valor de h
    final_distances = {}
    for u in distances:
        final_distances[u] = {}
        for v in distances[u]:
            final_distances[u][v] = distances[u][v] - h[u] + h[v]
    
    plt.show()  # Mantém o gráfico aberto até o final
    
    return final_distances, paths

# Função para criar e mostrar uma tabela com as distâncias e caminhos
def plot_distance_table(distances, paths):
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Prepara os dados para a tabela
    headers = [""] + list(distances.keys())  # Cabeçalho com os vértices
    table_data = []

    for u in distances:
        row = [u] + [f"{distances[u][v]} ({' -> '.join(paths[u][v])})" if u != v else "-" for v in distances[u]]  # Distâncias e caminhos
        table_data.append(row)

    # Cria e exibe a tabela
    table = ax.table(cellText=table_data, colLabels=headers, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Mostra a tabela
    plt.show()

# Define o grafo original
G = nx.DiGraph()
G.add_weighted_edges_from([
    ('A', 'B', 3), 
    ('A', 'C', 8), 
    ('B', 'C', 2), 
    ('B', 'D', 5),
    ('C', 'D', 1),
    ('D', 'A', -4)
])

# Executa o Algoritmo de Johnson e exibe a visualização
plt.ion()  # Ativa o modo interativo do matplotlib
shortest_paths, shortest_paths_routes = johnson_algorithm_visual(G)

# Mostra as distâncias finais em uma tabela
if shortest_paths:
    print("Distâncias mais curtas e caminhos entre todos os pares de vértices:")
    plt.ioff()  # Desativa o modo interativo para manter a tabela aberta
    plot_distance_table(shortest_paths, shortest_paths_routes)
