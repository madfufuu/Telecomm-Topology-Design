"""
descending_tree.py
    Module that contains the Descending Tree heuristics definition.
"""

import network
import utils


def GetKey(item):
    return item[1]


def DescendingTree(topology: network.Network):
    edge_dict = dict()
    edge_dist = []
    coords = topology.get_node_coords()
    count = 0
    for node_v in topology.get_network_graph().nodes:
        for node_e in topology.get_network_graph().nodes:
            if node_v != node_e and not topology.has_edge(node_v, node_e):
                topology.add_edge(node_v, node_e, weight=1)
                edge_dict[count] = (node_v, node_e)
                edge_dist.append((count, utils.euclidean_distance(
                                    coords[node_v], coords[node_e])))
                count = count + 1

    edge_dist = sorted(edge_dist, key=GetKey)
    edge_dist.reverse()
    final_state = False
    while not final_state:
        final_state = True
        for edge in edge_dist:
            coord1 = edge_dict[edge[0]][0]
            coord2 = edge_dict[edge[0]][1]
            topology.remove_edge(coord1, coord2)
            if topology.is_network_connected():
                if topology.check_network_connectivity(3):
                    if topology.check_network_diameter() <= 4:
                        final_state = False
                        edge_dist.remove(edge)
                        break

            topology.add_edge(edge_dict[edge[0]][0],
                              edge_dict[edge[0]][1], weight=1)
    return topology
