# -*- coding: utf-8 -*- 
# creating a new network 
import networkx as nx 

G = nx.Graph() 
N=[1,2,3,4,5,6,7,8,9,10]
E= [(1,2),(1,8),(2,3),(2,4),(4,5),(6,7),(6,8),(8,9),(8,10)]
G.add_nodes_from(N)
G.add_edges_from(E)
# drawing the created network 
import matplotlib.pyplot as plt

nx.draw_networkx(G,with_labels=True, node_color='r') 
plt.axis('off')
plt.title('an example')
plt.savefig("example.png") # save as png
plt.show() 