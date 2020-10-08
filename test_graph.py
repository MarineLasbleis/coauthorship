
import matplotlib.pyplot as plt
import networkx as nx



G = nx.Graph()
G.add_edge(1,2,color='r',weight=2)
G.add_edge(2,3,color='b',weight=4)
G.add_edge(3,4,color='g',weight=6)

pos = nx.circular_layout(G)

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]

nx.draw(G, pos, edge_color=colors, width=weights)




G = nx.random_geometric_graph(20, 0.5)
# position is stored as node attribute data for random_geometric_graph
pos = nx.get_node_attributes(G, "pos")

# find node near center (0.5,0.5)
dmin = 1
ncenter = 0
for n in pos:
    x, y = pos[n]
    d = (x - 0.5) ** 2 + (y - 0.5) ** 2
    if d < dmin:
        ncenter = n
        dmin = d

# color by path length from node near center
p = dict(nx.single_source_shortest_path_length(G, ncenter))
print(p.values())




plt.figure(figsize=(8, 8))
nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=list(p.keys()),
    node_size=80,
    node_color=list(p.values()),
    cmap=plt.cm.Reds_r,
)

plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)
plt.axis("off")



plt.figure(figsize=(8, 8))

G = nx.Graph()

authors = {'J Noir': 1, 'M Calkins': 1, 'M Lasbleis': 32, 'J Cantwell': 1, 'J Aurnou': 1, 'E Tasker': 1, 'J Tan': 1, 'K Heng': 1, 'S Kane': 1, 'D Spiegel': 1, 'R Brasser': 1, 'A Casey': 1, 'S Desch': 1, 'C Dorn': 1, 'J Hernlund': 5, 'C Houser': 1, 'M Laneuville': 1, 'A Libert': 1, 'L Noack': 3, 'C Unterborn': 1, 'J Wicks': 1, 'Z Geballe': 3, 'V Cormier': 2, 'E Day': 7, 'R Deguen': 7, 'P Cardin': 1, 'S Labrosse': 5, 'L Waszek': 6, 'M Kervazo': 4, 'G Choblet': 1, 'I Bonati': 1, 'K Hirose': 1, 'D Frost': 3, 'B Romanowicz': 2, 'B Chandler': 1, 'G Morard': 1, 'S Burdick': 1, 'W Anandawansha': 1, 'Q Forquenot': 1, 'D Al-Attar': 1, 'J Baptiste': 1, 'C Perge': 1, 'A Marguerite': 1, 'H Dore': 1, 'B Bourget': 1, 'M Youssof': 1, 'H Yue': 1}

G.add_nodes_from(authors.keys())

print(authors.values())

nx.draw(G, with_labels=True, node_size=[authors[k]*100 for k in authors])

plt.show()