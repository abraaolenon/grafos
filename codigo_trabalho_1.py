import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt


def get_pdf_and_ccdf(graph):
    """
    Calcula e exibe a PDF (Probability Distribution Function) e a CCDF (Complementary Cumulative Distribution Function) do grafo.
    Plota os resultados como gráficos para melhor visualização.

    Args:
        graph (networkx.Graph): O grafo para análise.

    Returns:
        None
    """
    # Obter os graus
    degrees = [degree for _, degree in graph.degree()]
    
    # Contar frequências dos graus
    degree_counts = Counter(degrees)
    
    # Calcular PDF
    total_nodes = len(graph)
    pdf = {k: v / total_nodes for k, v in degree_counts.items()}
    
    # Calcular CCDF
    sorted_degrees = sorted(pdf.keys())
    cumulative = 0
    ccdf = {}
    for degree in reversed(sorted_degrees):
        cumulative += pdf[degree]
        ccdf[degree] = cumulative
    ccdf = dict(sorted(ccdf.items()))  # Ordenar por grau
    
    # Exibir no console
    print("\n--- PDF ---")
    print(pdf)
    print("\n--- CCDF ---")
    print(ccdf)
    
    # Plotar PDF e CCDF
    plt.figure(figsize=(12, 5))
    
    # PDF
    plt.subplot(1, 2, 1)
    plt.bar(pdf.keys(), pdf.values(), color='blue', alpha=0.7)
    plt.title("PDF (Distribuição de Graus)")
    plt.xlabel("Grau")
    plt.ylabel("Probabilidade")
    
    # CCDF
    plt.subplot(1, 2, 2)
    plt.plot(ccdf.keys(), ccdf.values(), marker='o', color='red')
    plt.title("CCDF (Distribuição Cumulativa)")
    plt.xlabel("Grau")
    plt.ylabel("Probabilidade Acumulada")
    
    plt.tight_layout()
    plt.show()


def get_all_paths(graph, start_node, end_node):
    """
    Encontra e exibe todos os caminhos simples entre dois nós em um grafo, destacando-os graficamente.

    Args:
        graph (networkx.Graph): O grafo para análise.
        start_node: O nó inicial.
        end_node: O nó final.

    Returns:
        list: Uma lista contendo todos os caminhos simples entre os nós, se existirem.
    """
    try:
        # Verificar se os nós estão presentes no grafo
        if start_node not in graph or end_node not in graph:
            print(f"Os nós {start_node} ou {end_node} não estão presentes no grafo.")
            return []

        # Obter todos os caminhos simples entre os nós fornecidos
        all_paths = list(nx.all_simple_paths(graph, source=start_node, target=end_node))

        if not all_paths:
            # Se não houver caminhos, informa ao usuário e retorna uma lista vazia
            print(f"\nNão há caminhos simples de {start_node} para {end_node}.")
            return []

        # Exibir todos os caminhos encontrados no console
        print(f"\nTodos os caminhos simples de {start_node} para {end_node}:")
        for idx, path in enumerate(all_paths, start=1):
            print(f" {idx}. {' -> '.join(map(str, path))}")

        # Gerar posições para os nós no gráfico
        pos = nx.spring_layout(graph)  # Layout para o grafo
        plt.figure(figsize=(10, 8))

        # Definir cores dos nós
        colors_nodes = []
        for node in graph.nodes:
            if node == start_node:
                colors_nodes.append("red")  # Nó inicial em vermelho
            elif node == end_node:
                colors_nodes.append("yellow")  # Nó final em azul
            else:
                colors_nodes.append("lightgray")  # Outros nós em laranja

        # Desenhar o grafo inteiro
        nx.draw(
            graph, pos, with_labels=True, node_color=colors_nodes,
            edge_color="gray", node_size=800, font_size=10
        )

        # Destaque os caminhos encontrados
        for path in all_paths:
            path_edges = list(zip(path, path[1:]))  # Transformar o caminho em pares de arestas
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="blue", width=2)
            # Destacar os nós no caminho (sem sobrescrever os nós inicial e final)
            nx.draw_networkx_nodes(
                graph, pos, nodelist=[node for node in path if node not in [start_node, end_node]],
                node_color="lightgray", node_size=900
            )

        # Exibir o título no gráfico
        plt.title(f"Todos os caminhos simples de {start_node} para {end_node}")
        plt.show()

        return all_paths
    except nx.NetworkXError as e:
        # Tratar erros relacionados ao grafo (exemplo: nós inexistentes)
        print(f"Erro ao buscar caminhos: {e}")
        return []

def get_shortest_path(graph, start_node, end_node):
    """
    Encontra e exibe o menor caminho entre dois nós em um grafo.
    Destaca o caminho encontrado no grafo graficamente.

    Args:
        graph (networkx.Graph): O grafo para análise.
        start_node: O nó inicial.
        end_node: O nó final.

    Returns:
        list: Lista dos nós no menor caminho, se existir.
    """
    # Verificar se os nós existem no grafo
    if start_node not in graph:
        print(f"Erro: O nó {start_node} não está no grafo.")
        return None
    if end_node not in graph:
        print(f"Erro: O nó {end_node} não está no grafo.")
        return None

    try:
        # Encontrar o menor caminho
        shortest_path = nx.shortest_path(graph, source=start_node, target=end_node)
        print(f"O menor caminho de {start_node} para {end_node} é: {shortest_path}")

        # Plotar o grafo com o menor caminho destacado
        pos = nx.spring_layout(graph, seed=42)  # Usar seed para layout consistente
        plt.figure(figsize=(10, 8))

        # Configurar cores dos nós
        node_colors = []
        for node in graph.nodes:
            if node == start_node:
                node_colors.append("red")  # Nó inicial em vermelho
            elif node == end_node:
                node_colors.append("blue")  # Nó final em azul
            elif node in shortest_path:
                node_colors.append("orange")  # Nós do caminho em laranja
            else:
                node_colors.append("lightgray")  # Outros nós em cinza claro

        # Desenhar o grafo completo
        nx.draw(
            graph, pos, with_labels=True, node_color=node_colors,
            edge_color="gray", node_size=800, font_size=10
        )

        # Destaque para as arestas do menor caminho
        path_edges = list(zip(shortest_path, shortest_path[1:]))  # Arestas no caminho
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="red", width=2)

        plt.title(f"Menor Caminho de {start_node} para {end_node}")
        plt.show()

        return shortest_path

    except nx.NetworkXNoPath:
        # Tratar o caso onde não há caminho entre os nós
        print(f"Não existe caminho entre os vértices {start_node} e {end_node}.")
        return None

def get_average_path(graph):
    """
    Calcula e exibe a distância média entre todos os pares de vértices em um grafo.
    Para grafos desconectados, calcula a distância média em cada componente conectada separadamente.

    Args:
        graph (networkx.Graph): O grafo a ser analisado.

    Returns:
        None
    """
    try:
        if nx.is_connected(graph):
            # Grafo conectado: calcula a distância média global
            average_distance = nx.average_shortest_path_length(graph)
            print(f"A distância média entre todos os pares de vértices no grafo conectado é: {average_distance:.4f}")
        else:
            # Grafo desconectado: calcula a distância média por componente conectada
            print("O grafo não é conectado. Calculando a distância média para cada componente conectada:")
            for i, component in enumerate(nx.connected_components(graph), start=1):
                subgraph = graph.subgraph(component)
                avg_dist = nx.average_shortest_path_length(subgraph)
                print(f"- Componente {i} (vértices: {list(component)}): distância média = {avg_dist:.4f}")
    except nx.NetworkXError as e:
        print(f"Erro ao calcular a distância média: {e}")


def get_eccentricity(graph, vertex):
    """
    Calcula, exibe e destaca graficamente a excentricidade de um vértice em um grafo.
    Destaca o vértice inicial e o vértice mais distante graficamente.

    Args:
        graph (networkx.Graph): O grafo no qual o vértice está localizado.
        vertex: O vértice cuja excentricidade será calculada.

    Returns:
        tuple: A excentricidade do vértice e o nó mais distante, se existir.
    """
    try:
        # Verificar se o vértice está no grafo
        if vertex not in graph:
            print(f"Erro: O vértice {vertex} não está presente no grafo.")
            return None

        # Preparar para desenhar o grafo
        pos = nx.spring_layout(graph, seed=42)  # Layout consistente para o grafo
        plt.figure(figsize=(10, 8))

        eccentricity = None
        farthest_node = None

        if nx.is_connected(graph):
            # Para grafos conectados
            eccentricity = nx.eccentricity(graph, v=vertex)
            farthest_node = max(nx.shortest_path_length(graph, source=vertex).items(), key=lambda x: x[1])[0]
            print(f"A excentricidade do vértice {vertex} no grafo conectado é: {eccentricity}")

            # Configurar cores para destaque
            node_colors = [
                "red" if node == vertex else 
                "blue" if node == farthest_node else 
                "lightgray" 
                for node in graph.nodes
            ]

        else:
            # Para grafos desconectados, localizar a componente conectada relevante
            for component in nx.connected_components(graph):
                if vertex in component:
                    subgraph = graph.subgraph(component)
                    eccentricity = nx.eccentricity(subgraph, v=vertex)
                    farthest_node = max(nx.shortest_path_length(subgraph, source=vertex).items(), key=lambda x: x[1])[0]
                    print(f"A excentricidade do vértice {vertex} na componente {list(component)} é: {eccentricity}")

                    # Configurar cores para destaque
                    node_colors = [
                        "red" if node == vertex else 
                        "blue" if node == farthest_node else 
                        "lightgray" 
                        for node in graph.nodes
                    ]
                    break
            else:
                print(f"O vértice {vertex} não foi encontrado em nenhuma componente conectada do grafo.")
                return None

        # Desenhar o grafo com destaque para os nós
        nx.draw(
            graph, pos, with_labels=True, node_color=node_colors,
            edge_color="gray", node_size=800, font_size=10
        )

        plt.title(f"Excentricidade do Vértice {vertex}")
        plt.show()

        return eccentricity, farthest_node

    except nx.NetworkXError as e:
        # Capturar erros do NetworkX e exibi-los
        print(f"Erro ao calcular a excentricidade: {e}")
        return None




def get_diameter(graph):
    """
    Calcula, exibe e destaca graficamente o diâmetro de um grafo.
    Para grafos desconectados, calcula o diâmetro de cada componente conectada.

    Args:
        graph (networkx.Graph): O grafo para o qual o diâmetro será calculado.

    Returns:
        dict: Um dicionário com o diâmetro e os nós correspondentes para cada componente conectada.
    """
    try:
        pos = nx.spring_layout(graph, seed=42)  # Layout fixo para o grafo
        plt.figure(figsize=(10, 8))

        diameter_data = {}  # Para armazenar o diâmetro de cada componente conectada

        if nx.is_connected(graph):
            # Para grafos conectados
            diameter = nx.diameter(graph)
            eccentricity = nx.eccentricity(graph)
            farthest_nodes = max(eccentricity.items(), key=lambda x: x[1])
            node1 = farthest_nodes[0]
            node2 = max(nx.shortest_path_length(graph, source=node1).items(), key=lambda x: x[1])[0]
            
            print(f"Diâmetro do grafo conectado: {diameter} (Entre {node1} e {node2})")
            diameter_data["connected"] = {"diameter": diameter, "nodes": (node1, node2)}

            # Destacar graficamente
            node_colors = [
                "red" if node in [node1, node2] else "lightgray" for node in graph.nodes
            ]
            path_edges = list(zip(nx.shortest_path(graph, node1, node2), nx.shortest_path(graph, node1, node2)[1:]))
            nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=800, font_size=10)
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="blue", width=2)

        else:
            # Para grafos desconectados
            components = nx.connected_components(graph)
            for idx, component in enumerate(components, start=1):
                subgraph = graph.subgraph(component)
                diameter = nx.diameter(subgraph)
                eccentricity = nx.eccentricity(subgraph)
                farthest_nodes = max(eccentricity.items(), key=lambda x: x[1])
                node1 = farthest_nodes[0]
                node2 = max(nx.shortest_path_length(subgraph, source=node1).items(), key=lambda x: x[1])[0]

                print(f"Diâmetro da componente {idx} ({list(component)}): {diameter} (Entre {node1} e {node2})")
                diameter_data[idx] = {"diameter": diameter, "nodes": (node1, node2)}

                # Destacar graficamente
                node_colors = [
                    "red" if node in [node1, node2] else 
                    "lightgray" 
                    for node in graph.nodes
                ]
                path_edges = list(zip(nx.shortest_path(subgraph, node1, node2), nx.shortest_path(subgraph, node1, node2)[1:]))
                nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=800, font_size=10)
                nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color=f"C{idx % 10}", width=2)

        plt.title("Diâmetro do Grafo e Componentes Conectadas")
        plt.show()

        return diameter_data

    except nx.NetworkXError as e:
        print(f"Erro ao calcular o diâmetro: {e}")
        return None


def get_density(graph):
    """
    Calcula e exibe a densidade do grafo.

    Args:
        graph (networkx.Graph): O grafo para o qual a densidade será calculada.

    Returns:
        None
    """
    try:
        # Calcular a densidade do grafo
        density = nx.density(graph)

        # Exibir o resultado com formatação clara
        print(f"A densidade do grafo é: {density:.4f}")
    except nx.NetworkXError as e:
        print(f"Erro ao calcular a densidade: {e}")


def has_eulerian(graph):
    """
    Verifica se o grafo possui um ciclo Euleriano e exibe o resultado.

    Um ciclo Euleriano é um ciclo que percorre todas as arestas do grafo exatamente uma vez.

    Args:
        graph (networkx.Graph): O grafo a ser analisado.

    Returns:
        None
    """
    # Verificar se o grafo possui um ciclo Euleriano
    if nx.is_eulerian(graph):
        print("\nO grafo possui um ciclo Euleriano.")
        print("Condições atendidas: Grafo é conectado e todos os vértices têm grau par.")
    else:
        print("\nO grafo NÃO possui um ciclo Euleriano.")
        print("Verifique se o grafo atende as condições:")
        print("1. O grafo deve ser conectado.")
        print("2. Todos os vértices devem ter grau par.")


def has_hamiltonian(graph):
    """
    Verifica se o grafo possui um ciclo Hamiltoniano.
    
    Um ciclo Hamiltoniano é um ciclo que visita cada vértice exatamente uma vez e retorna ao vértice inicial.
    
    Parâmetros:
    graph (nx.Graph): O grafo a ser analisado.
    
    Retorno:
    None. Apenas imprime se o ciclo Hamiltoniano existe ou não.
    """
    
    def hamiltonian_path(visited, current, start):
        """
        Função recursiva para verificar a existência de um ciclo Hamiltoniano.

        Parâmetros:
        visited (set): Conjunto de nós já visitados.
        current (int): Nó atualmente sendo analisado.
        start (int): Nó de início para fechar o ciclo.

        Retorno:
        bool: Verdadeiro se um ciclo Hamiltoniano for encontrado.
        """
        # Caso base: Se todos os nós forem visitados, verifica se há aresta de retorno ao nó inicial
        if len(visited) == len(graph.nodes):
            return start in graph.neighbors(current)  # Verifica a conexão com o início do ciclo
        
        # Explora os vizinhos do nó atual
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:  # Se o vizinho ainda não foi visitado
                # Chamada recursiva com o vizinho adicionado aos visitados
                if hamiltonian_path(visited | {neighbor}, neighbor, start):
                    return True
        return False

    # Tenta iniciar um ciclo Hamiltoniano a partir de cada nó no grafo
    for node in graph.nodes:
        if hamiltonian_path({node}, node, node):  # Conjunto inicial contém apenas o nó de partida
            print("O grafo possui um ciclo Hamiltoniano.")
            return
    
    # Se nenhum ciclo Hamiltoniano for encontrado
    print("O grafo NÃO possui um ciclo Hamiltoniano.")


def get_all_cliques(grafo):
    """
    Identifica, exibe e destaca todos os cliques de um grafo de forma gráfica.

    Um clique é um subconjunto de vértices completamente conectado, ou seja,
    cada par de vértices do subconjunto possui uma aresta entre si.

    Args:
        grafo (nx.Graph): O grafo a ser analisado.

    Returns:
        list: Uma lista contendo todos os cliques no grafo.
    """
    # Obter a posição dos nós para visualização
    pos = nx.spring_layout(grafo, seed=42)  # Layout consistente com seed para repetibilidade
    
    # Identificar todos os cliques no grafo
    cliques = list(nx.find_cliques(grafo))
    
    print(f"Encontrados {len(cliques)} cliques no grafo:")
    print(cliques)

    # Configurar o tamanho da figura
    plt.figure(figsize=(10, 8))
    
    # Desenhar o grafo base
    nx.draw_networkx(
        grafo, 
        pos, 
        with_labels=True, 
        node_color="lightgray", 
        edge_color="gray", 
        node_size=800, 
        font_size=10
    )
    
    # Destaque de cada clique
    for i, clique in enumerate(cliques):
        # Subgrafo do clique
        clique_subgrafo = grafo.subgraph(clique)
        
        # Destaque os nós do clique
        nx.draw_networkx_nodes(
            grafo, 
            pos, 
            nodelist=clique, 
            node_color=f"C{i % 10}",  # Escolher cores cíclicas baseadas no índice
            node_size=900
        )
        
        # Destaque as arestas do clique
        nx.draw_networkx_edges(
            grafo, 
            pos, 
            edgelist=clique_subgrafo.edges(), 
            edge_color=f"C{i % 10}", 
            width=2
        )
    
    # Adicionar título ao gráfico
    plt.title("Grafos com Destaque para os Cliques")
    # Exibir o gráfico
    plt.show()

    # Retornar os cliques identificados
    return cliques

def get_clique_maximo(grafo):
    """
    Retorna o tamanho do clique máximo e os nós que o compõem.
    """
    cliques = list(nx.find_cliques(grafo))  # Encontra todos os cliques
    clique_maximo = max(cliques, key=len)  # Seleciona o maior clique
    print(f"Tamanho do clique máximo: {len(clique_maximo)}")
    

    """
    Plota o grafo com destaque para o clique máximo.
    """
    pos = nx.spring_layout(grafo)  # Layout para posicionar os nós
    plt.figure(figsize=(8, 6))

    # Desenhar o grafo inteiro
    nx.draw_networkx(grafo, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800, font_size=10)
    
    # Destaque o clique máximo
    nx.draw_networkx_nodes(grafo, pos, nodelist=clique_maximo, node_color="orange")
    clique_subgrafo = grafo.subgraph(clique_maximo)
    nx.draw_networkx_edges(grafo, pos, edgelist=clique_subgrafo.edges(), edge_color="orange", width=2)

    plt.title("Grafo com Destaque para o Clique Máximo")
    plt.show()


def get_totally_connected(grafo):
    """
    Verifica se o grafo é totalmente conectado e retorna o número de componentes conexos.
    """
    totalmente_conectado = nx.is_connected(grafo)  # Verifica se o grafo é conectado
    numero_componentes = nx.number_connected_components(grafo)  # Número de componentes conexos

    print(f"O grafo é totalmente conectado? {'Sim' if totalmente_conectado else 'Não'}")
    print(f"Número de componentes conexos: {numero_componentes}")
    
    """
    Plota o grafo, destacando cada componente conexo com uma cor diferente.
    """
    pos = nx.spring_layout(grafo)  # Layout para posicionar os nós
    plt.figure(figsize=(8, 6))
    
    # Obter as componentes conexas
    componentes = list(nx.connected_components(grafo))
    
    # Desenhar o grafo com cores para cada componente
    for i, componente in enumerate(componentes):
        subgrafo = grafo.subgraph(componente)
        nx.draw_networkx(subgrafo, pos, node_color=f"C{i % 10}", with_labels=True, node_size=800, font_size=10)

    plt.title("Componentes Conexos no Grafo")
    plt.show()

def check_isomorphic(grafo1, grafo2):
    """
    Verifica se dois grafos são isomórficos e exibe suas representações gráficas.

    Dois grafos são isomórficos se existe uma correspondência entre seus nós e arestas,
    preservando a estrutura do grafo.

    Args:
        grafo1 (networkx.Graph): O primeiro grafo para análise.
        grafo2 (networkx.Graph): O segundo grafo para análise.

    Returns:
        bool: True se os grafos são isomórficos, False caso contrário.
    """
    # Verificar se os grafos são isomórficos
    is_isomorphic = nx.is_isomorphic(grafo1, grafo2)
    print(f"Os grafos são isomórficos? {'Sim' if is_isomorphic else 'Não'}")

    # Configurar layout consistente para os dois grafos
    pos1 = nx.spring_layout(grafo1, seed=42)
    pos2 = nx.spring_layout(grafo2, seed=42)

    # Desenhar o primeiro grafo
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    nx.draw(
        grafo1,
        pos1,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=800,
        font_size=10,
    )
    plt.title("p2p-Gnutella09")

    # Desenhar o segundo grafo
    plt.subplot(122)
    nx.draw(
        grafo2,
        pos2,
        with_labels=True,
        node_color="lightgreen",
        edge_color="gray",
        node_size=800,
        font_size=10,
    )
    plt.title("p2p-Gnutella08")

    # Exibir gráficos
    plt.suptitle("Comparação de Grafos")
    plt.tight_layout()
    plt.show()

    return is_isomorphic


def get_bigger_component(graph):
    """
    Retorna o conjunto de nós da maior componente conexa e plota o grafo com destaque.

    Args:
        graph (networkx.Graph): O grafo para análise.

    Returns:
        None
    """
    componentes = list(nx.connected_components(graph))  # Lista de componentes conexas
    maior_componente = max(componentes, key=len)  # Seleciona a maior componente
    
    print(f"\nNós na maior componente conexa: {maior_componente}")
    
    # Plotar o grafo com destaque para a maior componente
    pos = nx.spring_layout(graph)  # Layout para posicionar os nós
    plt.figure(figsize=(8, 6))

    # Desenhar o grafo inteiro
    nx.draw_networkx(graph, pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=800, font_size=10)
    
    # Destaque para a maior componente
    subgrafo = graph.subgraph(maior_componente)
    nx.draw_networkx_nodes(subgrafo, pos, node_color="orange", node_size=800)
    nx.draw_networkx_edges(subgrafo, pos, edge_color="orange", width=2)

    plt.title("Maior Componente Conexa no Grafo")
    plt.tight_layout()
    plt.show()


def get_bridges(graph):
    """
    Identifica e destaca visualmente as pontes (bridges) em um grafo.

    Uma ponte é uma aresta cuja remoção desconecta uma parte do grafo.

    Args:
        graph (networkx.Graph): O grafo para análise.

    Returns:
        list: Uma lista de tuplas representando as pontes no grafo.
    """
    try:
        # Identificar as pontes no grafo
        bridges = list(nx.bridges(graph))
        print(f"\nPontes encontradas: {bridges}")

        # Configurar a posição dos nós
        pos = nx.spring_layout(graph, seed=42)  # Layout consistente para melhor visualização
        
        # Configurar o tamanho da figura
        plt.figure(figsize=(10, 8))

        # Desenhar o grafo base
        nx.draw_networkx(
            graph, 
            pos, 
            with_labels=True, 
            node_color="lightblue", 
            edge_color="gray", 
            node_size=800, 
            font_size=10
        )

        # Destaque as pontes no grafo
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=bridges,
            edge_color="red",
            width=2,
        )

        # Adicionar título e legenda
        plt.title("Grafo com Pontes Destacadas")
        plt.show()

        return bridges

    except nx.NetworkXError as e:
        print(f"Erro ao identificar as pontes: {e}")
        return []

def ler_grafo_nao_direcionado(caminho_arquivo):
    """
    Lê um arquivo de texto no formato de pares de nós e cria um grafo não direcionado.

    Formato esperado:
    # Comentários começam com "#"
    FromNodeId	ToNodeId
    0	1
    0	2
    ...

    Parâmetros:
    caminho_arquivo (str): Caminho para o arquivo de texto.

    Retorno:
    nx.Graph: Grafo não direcionado criado a partir do arquivo.
    """
    grafo = nx.Graph()  # Cria um grafo não direcionado
    quantidade_linha=0

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if quantidade_linha == 100: # Limita a leitura do arquivo
                break
            # Ignora comentários ou linhas em branco
            linha = linha.strip()
            if linha.startswith("#") or not linha:
                continue
            
            # Divide a linha em nós de origem e destino
            origem, destino = map(int, linha.split())
            grafo.add_edge(origem, destino)  # Adiciona uma aresta não direcionada
            quantidade_linha = quantidade_linha+1
    
    return grafo


def mostrar_grafo(grafo):
    print("Desenhando o grafo....")
    nx.draw(grafo, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800, font_size=10)
    plt.title("Exemplo de Grafo")
    plt.show()


print("*************************** Respostas do Trabalho 1 ***************************")
print("\n Aluno: Abraão Lenon Moreira de Oliveira")
print("\n 1) Escolha dos datasets.")
print("Datasets escolhidos: ")
print("https://snap.stanford.edu/data/p2p-Gnutella09.html")
print("https://snap.stanford.edu/data/p2p-Gnutella08.html")

print("Lendo os datasets......")

graph = ler_grafo_nao_direcionado("/home/abraaolenon/Desktop/Mestrado/p2p-Gnutella09.txt")
graph08 = ler_grafo_nao_direcionado("/home/abraaolenon/Desktop/Mestrado/p2p-Gnutella08.txt")


print("\n 2) Quanto à distribuição dos graus dos grafos, calcular: PDF (Probability Distribution Function) e a CCDF (Complementary Cumulative Distribution Function).")
get_pdf_and_ccdf(graph)

print("\n 3) A partir da escolha de 2 vértices, determinar todos os possíveis caminhos entre eles.")
get_all_paths(graph, 21, 4)

print("\n 4) A partir da escolha de 2 vértices, determinar o menor caminho.")
get_shortest_path(graph, 703, 11)

print("\n 5) Determinar a distância média entre todos os pares de vértices.")
get_average_path(graph)

print("\n 6) A partir da escolha de um vértice, determinar a excentricidade")
get_eccentricity(graph, 1)

print("\n 7) Determinar o diâmetro da rede.")
get_diameter(graph)

print("\n 8) Determinar a densidade dos grafos.")
get_density(graph)

print("\n 9) Verificar a existência de ciclos Eulerianos e Hamiltonianos nos Grafos.")
has_eulerian(graph)
has_hamiltonian(graph)

print("\n 10) Retornar todos os cliques em um grafo.")
get_all_cliques(graph)

print("\n 11) Retornar o clique máximo em um grafo.")
get_clique_maximo(graph)

print("\n 12) Identificar se o grafo é totalmente conectado e retornar o número de componentes.")
get_totally_connected(graph)

print("\n 13) Retornar o conjunto de nós da maior componente.")
get_bigger_component(graph)

print("\n 14) Verificar se dois Grafos são Isomórficos.")
check_isomorphic(graph, graph08)

print("\n 15) Verificar a existência de bridges nos grafos.")
get_bridges(graph)
