"""
network.py
    Module that contains the Network class definition.
"""

import matplotlib.pyplot as plt
import networkx as nx
import random
import utils


class Network:
    """
    Network Class
        Abstracted class for the Network Topology problem, underlying structure
        implemented using Networkx's Graph class.
    """
    n = 0
    graph = nx.Graph()
    coords = dict()

    def __init__(self, n):
        self.graph = nx.Graph()
        self.n = n
        self.init_network_with_random_nodes()

    def init_network_with_random_nodes(self):
        for node in range(self.n):
            x_coord = random.randint(1, 100)
            y_coord = random.randint(1, 100)
            while [x_coord, y_coord] in self.coords.values():
                x_coord = random.randint(1, 100)
                y_coord = random.randint(1, 100)
            self.coords[node] = [x_coord, y_coord]
            self.graph.add_node(node, coords=(x_coord, y_coord))

    def reinitialize_network(self):
        self.graph = nx.Graph()
        for node in self.coords:
            self.graph.add_node(node, coords=self.coords[node])

    def add_edge(self, v, e, weight):
        self.graph.add_edge(v, e, weight=weight)

    def remove_edge(self, v, e):
        self.graph.remove_edge(v, e)

    def has_edge(self, v, e):
        return self.graph.has_edge(v, e)

    def get_network_graph(self):
        return self.graph

    def is_network_connected(self):
        return nx.is_connected(self.graph)

    def check_network_connectivity(self, k):
        return nx.is_k_edge_connected(self.graph, k)

    def check_network_diameter(self):
        return nx.diameter(self.graph)

    def check_node_eccentricity(self):
        return nx.eccentricity(self.graph)

    def get_node_connected_component(self, n):
        return nx.node_connected_component(self.graph, n)

    def get_connected_subnetwork(self):
        return [self.graph.subgraph(c).copy()
                for c in nx.connected_components(self.graph)]

    def get_node_neighbors(self, n):
        return list(nx.neighbors(self.graph, n))

    def get_node_coords(self):
        return self.coords

    def draw_network(self):
        pos = nx.get_node_attributes(self.graph, "coords")
        nx.draw(self.graph, pos, with_labels=True)
        plt.show(block=True)

    def get_total_network_cost(self):
        total_cost = 0
        for edge in self.graph.edges:
            total_cost += utils.euclidean_distance(
                            self.coords.get(edge[0]),
                            self.coords.get(edge[1])
                        )
        return round(total_cost, 2)
