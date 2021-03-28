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
from geopy.geocoders import Nominatim

imsize = np.array([1600, 1200])
place_name = "Lund, Skåne, Sweden"
graph = ox.graph_from_place(place_name, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph)
fig, ax = ox.plot_graph(graph, figsize=imsize/100, show=False)

loc = "Kämnärsvägen 42, Skåne, Sweden"
geolocator = Nominatim(user_agent="my_request")
location = geolocator.geocode(loc)

print(location.address)
# ax.plot(location.longitude, location.latitude, marker='o', markersize=10,
#                     markerfacecolor="red", markeredgecolor="red")
ax.plot(13.217381969757525, 55.72105809999999, marker='o', markersize=10,
                    markerfacecolor="red", markeredgecolor="red")
print(ax.get_xlim())
print(ax.get_ylim())

plt.show()
# d="M 212.155699 768.96 L 968.644301 768.96 L 968.644301 103.68 L 212.155699 103.68 z "
# fig.savefig("lund-map.svg")
