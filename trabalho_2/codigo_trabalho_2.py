import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Lista de colaborações fictícias (FromNodeId, ToNodeId)
edges = [
    ("Alice", "Bob"), ("Alice", "Carol"), ("Alice", "Dave"), ("Bob", "Eve"),
    ("Bob", "Frank"), ("Carol", "Grace"), ("Carol", "Hannah"), ("Dave", "Ivy"),
    ("Eve", "Jack"), ("Frank", "Grace"), ("Frank", "Hannah"), ("Grace", "Ivy"),
    ("Hannah", "Jack"), ("Ivy", "Kevin"), ("Jack", "Laura"), ("Kevin", "Mike"),
    ("Laura", "Nancy"), ("Mike", "Oscar"), ("Nancy", "Paul"), ("Oscar", "Quincy"),
    ("Paul", "Rachel"), ("Quincy", "Steve"), ("Rachel", "Tracy"), ("Steve", "Uma"),
    ("Tracy", "Victor"), ("Uma", "Wendy"), ("Victor", "Xander"), ("Wendy", "Yvonne"),
    ("Xander", "Zane"), ("Yvonne", "Alice"), ("Zane", "Bob"), ("Alice", "Kevin"),
    ("Bob", "Laura"), ("Carol", "Mike"), ("Dave", "Nancy"), ("Eve", "Oscar"),
    ("Frank", "Paul"), ("Grace", "Quincy"), ("Hannah", "Rachel"), ("Ivy", "Steve"),
    ("Jack", "Tracy"), ("Kevin", "Uma"), ("Laura", "Victor"), ("Mike", "Wendy"),
    ("Nancy", "Xander"), ("Oscar", "Yvonne"), ("Paul", "Zane"), ("Quincy", "Alice"),
    ("Rachel", "Bob"), ("Steve", "Carol"), ("Alice", "Nancy"), ("Eve", "Laura"),
    ("Mike", "Grace"), ("Zane", "Victor"), ("Oscar", "Steve"), ("Tracy", "Bob"),
    ("Uma", "Carol"), ("Victor", "Eve"), ("Wendy", "Grace"), ("Xander", "Alice"),
    ("Yvonne", "Mike"), ("Alice", "Quincy"), ("Dave", "Uma"), ("Laura", "Paul"),
    ("Ivy", "Frank"), ("Grace", "Hannah"), ("Zane", "Nancy"), ("Bob", "Oscar"),
    ("Quincy", "Hannah"), ("Tracy", "Steve"), ("Wendy", "Victor"), ("Xander", "Rachel"),
    ("Mike", "Laura"), ("Kevin", "Ivy"), ("Alice", "Hannah"), ("Nancy", "Oscar"),
    ("Carol", "Xander"), ("Paul", "Uma"), ("Laura", "Quincy"), ("Grace", "Tracy"),
    ("Kevin", "Yvonne"), ("Victor", "Alice"), ("Nancy", "Bob"), ("Oscar", "Jack"),
    ("Tracy", "Carol"), ("Rachel", "Dave"), ("Ivy", "Steve"), ("Grace", "Quincy"),
    ("Frank", "Zane"), ("Mike", "Hannah"), ("Bob", "Laura"), ("Nancy", "Yvonne"),
    ("Victor", "Oscar"), ("Paul", "Kevin"), ("Quincy", "Steve"), ("Grace", "Victor")
]

# Criando um DataFrame para visualizar as conexões em forma de tabela
df = pd.DataFrame(edges, columns=["FromNodeId", "ToNodeId"])
print("Lista de conexões:")
print(df)

# Criando o grafo com NetworkX
G = nx.Graph()
G.add_edges_from(edges)

# Definindo as cores para os nós
node_color = []
for node in G.nodes():
    if node == "Alice":
        node_color.append("red")  # Cor para o nó "Alice"
    elif node == "Bob":
        node_color.append("yellow")  # Cor para o nó "Bob"
    elif node == "Victor":
        node_color.append("green") # Cor para o nó "Victor"
    elif node == "Oscar":
        node_color.append("green") # Cor para o nó "Oscar"
    else:
        node_color.append("lightblue")  # Cor para os outros nós


# Desenhando o grafo para visualização
plt.figure(figsize=(12, 10))  # Configurando o tamanho da figura
nx.draw_networkx(
    G,
    with_labels=True,  # Exibir os nomes dos nós
    node_color=node_color,  # Cor dos nós
    edge_color="gray",  # Cor das arestas
    node_size=700,  # Tamanho dos nós
    font_size=8  # Tamanho da fonte dos rótulos
)

# Contando nós e arestas
num_nos = G.number_of_nodes()
num_arestas = G.number_of_edges()

# Adicionando o número de nós e arestas ao título
plt.title(f"Rede de Colaboração entre Pesquisadores\n"
          f"Nós: {num_nos} | Arestas: {num_arestas}")
plt.show()

# Função para ordenar e obter os 10 maiores valores
def top_10_centrality(measure):
    return sorted(measure.items(), key=lambda x: x[1], reverse=True)[:10]


# Calculando medidas de centralidade
# 1. Centralidade de Grau (Degree Centrality): Mede o número de conexões diretas de cada pesquisador
degree_centrality = nx.degree_centrality(G)
print("\nDegree Centrality (Centralidade de Grau):")
for researcher, value in top_10_centrality(degree_centrality):
    print(f"{researcher}: {value:.4f}")


# 2. Centralidade de Proximidade (Closeness Centrality): Mede a proximidade de um nó com todos os outros
closeness_centrality = nx.closeness_centrality(G)
print("\nCloseness Centrality (Centralidade de Proximidade):")
for researcher, value in top_10_centrality(closeness_centrality):
    print(f"{researcher}: {value:.4f}")


# 3. Centralidade de Intermediação (Betweenness Centrality): Mede quantas vezes um nó está nos caminhos mais curtos
betweenness_centrality = nx.betweenness_centrality(G)
print("\nBetweenness Centrality (Centralidade de Intermediação):")
for researcher, value in top_10_centrality(betweenness_centrality):
    print(f"{researcher}: {value:.4f}")


# 4. Centralidade de Autovetor (Eigenvector Centrality): Mede a importância de um nó baseado nos seus vizinhos
eigenvector_centrality = nx.eigenvector_centrality(G)
print("\nEigenvector Centrality (Centralidade de Autovetor):")
for researcher, value in top_10_centrality(eigenvector_centrality):
    print(f"{researcher}: {value:.4f}")


# 5. Centralidade de Katz (Katz Centrality): Considera conexões diretas e indiretas com penalização para conexões mais distantes
katz_centrality = nx.katz_centrality(G, alpha=0.1, beta=1.0)
print("\nKatz Centrality (Centralidade de Katz):")
for researcher, value in top_10_centrality(katz_centrality):
    print(f"{researcher}: {value:.4f}")


