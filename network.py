#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creating a new network

import networkx as nx
import pandas as pd
import numpy as np

num_client = 15
capacity = 100
randint = np.random.randint

df = pd.DataFrame({"x": randint(0, 100, num_client),
                   "y": randint(0, 100, num_client),
                   "d": randint(5, 40, num_client)})

df.ix[0].x = 50
df.ix[0].y = 50
df.ix[0].d = 0

G = nx.Graph()

N = []
for i in range(num_client):
    N.append(i)

pos = {}
for position in range(num_client):
    pos[N[position]] = (df.ix[position].x, df.ix[position].y)


E =[]
E.append((2,3))
E.append((5,8))
#E= [(1,2),(1,8),(2,3),(2,4),(4,5),(6,7),(6,8),(8,9),(8,10)]
edge_labels ={}

edge_labels[(2,3)] = 4

G.add_nodes_from(N)
G.add_edges_from(E)


# drawing the created network
import matplotlib.pyplot as plt



nx.draw_networkx(G,pos, node_color='r',node_size=150)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11)

plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(-5, 105)
plt.ylim(-5, 105)
# plt.axis('off')
plt.title('an example')
plt.savefig("example.png")  # save as png
plt.grid()
plt.show()
