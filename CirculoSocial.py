import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

G = nx.Graph()

MI_NOMBRE = "Karlos (Centro)"
G.add_node(MI_NOMBRE)

comunidades = {
    "Familia": ["Mamá", "Papá", "Hermano", "Hermana"],
    "Amigos Barrio": ["David", "Gabriela", "Carmelo"],
    "Compañeros Universidad": ["Danna", "Javier", "Daniel", "Carlos"]
}

colores_comunidad = {
    "Centro": "#FF4500",
    "Familia": "#1F77B4",
    "Amigos Barrio": "#2CA02C",
    "Compañeros Universidad": "#9467BD"
}

mapa_colores = {MI_NOMBRE: colores_comunidad["Centro"]}

for com_nombre, miembros in comunidades.items():
    color = colores_comunidad[com_nombre]
    for miembro in miembros:
        G.add_node(miembro)
        mapa_colores[miembro] = color
        G.add_edge(MI_NOMBRE, miembro)

familia = comunidades["Familia"]
for i in range(len(familia)):
    for j in range(i + 1, len(familia)):
        G.add_edge(familia[i], familia[j])

G.add_edge("David", "Gabriela")
G.add_edge("David", "Carmelo")

uni = comunidades["Compañeros Universidad"]
for i in range(len(uni)):
    for j in range(i + 1, len(uni)):
        G.add_edge(uni[i], uni[j])

# Matriz de adyacencia
nodos = list(G.nodes())
matriz_adyacencia = nx.to_numpy_array(G, nodelist=nodos)
df_matriz = pd.DataFrame(matriz_adyacencia, index=nodos, columns=nodos, dtype=int)

print("=" * 65)
print("MATRIZ DE ADYACENCIA DE LA RED SOCIAL")
print("=" * 65)
print(df_matriz)
print("=" * 65)

pos = {}
pos[MI_NOMBRE] = np.array([0, 0])

angulos_base = {
    "Familia": np.pi * 5 / 6,              
    "Amigos Barrio": np.pi / 6,             
    "Compañeros Universidad": -np.pi / 2    
}

radio = 2.5

for com_nombre, miembros in comunidades.items():
    angulo_centro = angulos_base[com_nombre]
    n = len(miembros)
    apertura = np.pi / 3
    angulos = np.linspace(angulo_centro - apertura/2, angulo_centro + apertura/2, n)
    
    for i, miembro in enumerate(miembros):
        pos[miembro] = np.array([radio * np.cos(angulos[i]), radio * np.sin(angulos[i])])

# Visualización
plt.figure(figsize=(10, 10))

colores_nodos = [mapa_colores[nodo] for nodo in G.nodes()]
tamaños_nodos = [3500 if nodo == MI_NOMBRE else 1800 for nodo in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_size=tamaños_nodos, node_color=colores_nodos, alpha=0.95)
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_family="sans-serif")

for com_nombre, color in colores_comunidad.items():
    if com_nombre != "Centro":
        plt.scatter([], [], color=color, label=com_nombre, s=120)

plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Comunidades", loc="upper left")
plt.title(f"Red Social Personal de {MI_NOMBRE}", fontsize=14, fontweight="bold")
plt.axis("off")
plt.xlim(-3.5, 3.5)
plt.ylim(-3.5, 3.5)
plt.tight_layout()

plt.show()
