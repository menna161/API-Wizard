import time
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString


def project_graph(G, to_crs=None):
    '\n    https://github.com/gboeing/osmnx/blob/v0.9/osmnx/projection.py#L126\n    Project a graph from lat-long to the UTM zone appropriate for its geographic\n    location.\n    Parameters\n    ----------\n    G : networkx multidigraph\n        the networkx graph to be projected\n    to_crs : dict\n        if not None, just project to this CRS instead of to UTM\n    Returns\n    -------\n    networkx multidigraph\n    '
    G_proj = G.copy()
    start_time = time.time()
    (nodes, data) = zip(*G_proj.nodes(data=True))
    gdf_nodes = gpd.GeoDataFrame(list(data), index=nodes)
    gdf_nodes.crs = G_proj.graph['crs']
    gdf_nodes.gdf_name = '{}_nodes'.format(G_proj.name)
    gdf_nodes['lon'] = gdf_nodes['x']
    gdf_nodes['lat'] = gdf_nodes['y']
    gdf_nodes['geometry'] = gdf_nodes.apply((lambda row: Point(row['x'], row['y'])), axis=1)
    gdf_nodes_utm = project_gdf(gdf_nodes, to_crs=to_crs)
    edges_with_geom = []
    for (u, v, key, data) in G_proj.edges(keys=True, data=True):
        if ('geometry' in data):
            edges_with_geom.append({'u': u, 'v': v, 'key': key, 'geometry': data['geometry']})
    if (len(edges_with_geom) > 0):
        gdf_edges = gpd.GeoDataFrame(edges_with_geom)
        gdf_edges.crs = G_proj.graph['crs']
        gdf_edges.gdf_name = '{}_edges'.format(G_proj.name)
        gdf_edges_utm = project_gdf(gdf_edges, to_crs=to_crs)
    start_time = time.time()
    gdf_nodes_utm['x'] = gdf_nodes_utm['geometry'].map((lambda point: point.x))
    gdf_nodes_utm['y'] = gdf_nodes_utm['geometry'].map((lambda point: point.y))
    gdf_nodes_utm = gdf_nodes_utm.drop('geometry', axis=1)
    start_time = time.time()
    edges = list(G_proj.edges(keys=True, data=True))
    graph_name = G_proj.graph['name']
    G_proj.clear()
    G_proj.add_nodes_from(gdf_nodes_utm.index)
    attributes = gdf_nodes_utm.to_dict()
    for label in gdf_nodes_utm.columns:
        nx.set_node_attributes(G_proj, name=label, values=attributes[label])
    for (u, v, key, attributes) in edges:
        if ('geometry' in attributes):
            row = gdf_edges_utm[(((gdf_edges_utm['u'] == u) & (gdf_edges_utm['v'] == v)) & (gdf_edges_utm['key'] == key))]
            attributes['geometry'] = row['geometry'].iloc[0]
        G_proj.add_edge(u, v, **attributes)
    G_proj.graph['crs'] = gdf_nodes_utm.crs
    G_proj.graph['name'] = '{}_UTM'.format(graph_name)
    if ('streets_per_node' in G.graph):
        G_proj.graph['streets_per_node'] = G.graph['streets_per_node']
    return G_proj
