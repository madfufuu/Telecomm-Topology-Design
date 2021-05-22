"""
greedy_3_tree.py
    Module that contains the Greedy 3 Tree heuristics definition.
"""

import network
import sys
import utils
import numpy as np


def Greedy3Tree(topology: network.Network):
    mid_points = MinDistance3Connected(topology)
    mid_point_pairs = MidPoint6Connected(topology, mid_points)
    MidPoint12Connected(topology, mid_point_pairs)
    MidPointAllConnected(topology, mid_points)

    return topology


def MinDistance3Connected(net):
    mid_points = []
    visited_nodes = [False] * len(net.get_network_graph().nodes)
    closest = sys.maxsize
    second_closest = sys.maxsize
    closest_index = -1

    for node_v in net.get_network_graph().nodes(data="coords"):
        if not visited_nodes[node_v[0]]:
            closest = sys.maxsize
            closest_index = -1
            second_closest_index = -1

            for node_e in net.get_network_graph().nodes(data="coords"):
                if node_v[0] is not node_e[0] and not visited_nodes[node_e[0]]:
                    dist = utils.euclidean_distance(node_v[1], node_e[1])
                    if dist < closest:
                        second_closest_index = closest_index
                        second_closest = closest
                        closest_index = node_e[0]
                        closest = dist
                    else:
                        if dist < second_closest:
                            second_closest_index = node_e[0]
                            second_closest = dist

            if closest_index != -1:
                net.add_edge(node_v[0], closest_index, weight=1)
                visited_nodes[closest_index] = True
                visited_nodes[node_v[0]] = True
                if second_closest_index != -1:
                    net.add_edge(node_v[0], second_closest_index, weight=1)
                    visited_nodes[second_closest_index] = True
                    mid_points.append(node_v)
    return mid_points


def MidPoint6Connected(net, mid_points):
    mid_point_pairs = []
    visited_nodes = [False] * len(net.get_network_graph().nodes)
    closest = sys.maxsize
    closest_index = -1

    for mid_point in mid_points:
        if not visited_nodes[mid_point[0]]:
            for node in net.get_node_connected_component(mid_point[0]):
                visited_nodes[node] = True
            closest_index = -1
            closest = sys.maxsize
            for node in mid_points:
                if mid_point[0] != node[0] and not visited_nodes[node[0]]:
                    dist = utils.euclidean_distance(mid_point[1], node[1])
                    if dist < closest:
                        closest = dist
                        closest_index = node[0]

            if closest_index != -1:
                net.add_edge(mid_point[0], closest_index, weight=1)
                for node in net.get_node_connected_component(mid_point[0]):
                    visited_nodes[node] = True
                mid_point_pairs.append((mid_point[0], closest_index))

    return mid_point_pairs


def MidPoint12Connected(net, mid_point_pairs):
    visited_nodes = [False] * len(net.get_network_graph().nodes)
    coords = net.get_node_coords()
    closest = sys.maxsize
    closest_index = (-1, -1)

    for pair in mid_point_pairs:
        if not visited_nodes[pair[0]]:
            closest = sys.maxsize
            closest_index = (-1, -1)
            for pair_2 in mid_point_pairs:
                if pair[0] != pair_2[0] and not visited_nodes[pair_2[0]]:
                    dist = utils.euclidean_distance(
                        coords.get(pair[0]), coords.get(pair_2[0])) + \
                        utils.euclidean_distance(
                            coords.get(pair[1]), coords.get(pair_2[1]))
                    if dist < closest:
                        closest = dist
                        closest_index = pair_2

            if closest_index != (-1, -1):
                net.add_edge(pair[0], closest_index[0], weight=1)
                net.add_edge(pair[1], closest_index[1], weight=1)
                for node in net.get_node_connected_component(pair[0]):
                    visited_nodes[node] = True


def MidPointAllConnected(net, mid_points):
    visited_nodes = [[False] * len(net.get_network_graph().nodes)
                     for _ in range(len(net.get_connected_subnetwork()))]

    for i, subgraph in enumerate(net.get_connected_subnetwork()):
        for node in subgraph:
            visited_nodes[i][node] = True

    for i, subgraph in enumerate(net.get_connected_subnetwork()):
        for node in subgraph.nodes:
            if len(net.get_node_neighbors(node)) < 3:
                for mid_point in mid_points:
                    if not visited_nodes[i][mid_point[0]]:
                        net.add_edge(node, mid_point[0], weight=1)

                while len(net.get_node_neighbors(node)) < 3:
                    coords = net.get_node_coords()
                    closest = sys.maxsize
                    closest_index = -1
                    neighbors = list(net.get_node_neighbors(node))
                    nc_list = np.setdiff1d(
                                list(net.get_network_graph().nodes), neighbors)
                    for n in nc_list:
                        if node != n:
                            dist = utils.euclidean_distance(coords.get(node),
                                                            coords.get(n))

                            if dist < closest:
                                closest = dist
                                closest_index = n
                    if closest_index != -1:
                        net.add_edge(node, closest_index, weight=1)
