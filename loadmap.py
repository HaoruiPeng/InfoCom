import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import networkx as nx
import base64
from io import BytesIO
from flask import Flask
from flask_cors import CORS


place_name = "Lund, Skåne, Sweden"
graph = ox.graph_from_place(place_name, network_type='drive')

# graph = ox.graph_from_place(place_name, network_type='bike')
# print(type(graph))
# nx.draw(graph, arrows=False, node_size=5, cmap='gist_gray')
# plt.draw()
# plt.show()

# nodes, edges = ox.graph_to_gdfs(graph,node_geometry=False, fill_edge_geometry=False)
nodes, edges = ox.graph_to_gdfs(graph)
# print(nodes.head())
# nodes.plot(markersize=1)
# edges.plot()
# plt.show()
# nodes_df = pd.DataFrame(nodes.drop(columns=['highway', 'ref']))
# edges_df= pd.DataFrame(edges.drop(columns=['oneway', 'lanes', 'ref', 'highway', 'maxspeed', 'bridge', 'tunnel', 'access', 'junction', 'width']))
#

# edge_geometry = edges_df['geometry']

# edge_list = edge_geometry.to_numpy()
# line = edge_list[0]
# print(line.coords[:])

# node_list = node_geometry.to_numpy()
# for n in node_list:
    # print(n.x, n.y)
    # input()



# fig, ax = ox.plot_graph(graph, show=False)
# plt.tight_layout()
# added_nodes=[(13.1928074, 55.7091421), (13.1928088, 55.7092004), (13.1928101, 55.7092525), (13.192811, 55.7092918), (13.1928062, 55.709616), (13.1928076, 55.709693), (13.1927816, 55.7098479), (13.1927591, 55.7100277), (13.1927393, 55.7101775), (13.1927575, 55.7103608)]
# x = [i[0] for i in added_nodes]
# y = [i[1] for i in added_nodes]
# ax.plot(x,y,color='red', marker='.')
# plt.show()
