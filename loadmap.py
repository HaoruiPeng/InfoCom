import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib import image, patches, colors
from matplotlib.colors import colorConverter
import matplotlib.animation as animation
import mpld3
import numpy as np
from mpld3 import plugins
import pandas as pd
import geopandas as gpd
import networkx as nx
import base64

imsize = np.array([1600, 1200])
place_name = "Lund, Skåne, Sweden"
graph = ox.graph_from_place(place_name, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph)
fig, ax = ox.plot_graph(graph, figsize=imsize/100, show=False)

plt.show()
fig.savefig("lund-map.svg")
