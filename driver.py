"""
driver.py
Driver program for atn-project3, comparison of two heuristic algorithms for a
network topology problem.
"""


import network
import sys
import logging
from timeit import time as timer
import greedy_3_tree
import descending_tree


def start(args):
    try:
        n = int(args[1])
    except ValueError:
        logging.exception("Program Usage: input 15 <= n <= 100,"
                          " the number of nodes in network.")
        sys.exit(1)
    except IndexError:
        logging.exception("Program Usage: input 15 <= n <= 100,"
                          " the number of nodes in network.",)
        sys.exit(1)

    if n < 15 or n > 100:
        print("Program Usage: input 15 <= n <= 100,"
              "the number of nodes in network.")
        sys.exit(1)

    # Initialize network
    nw = network.Network(n)

    # Greedy3Tree run
    start_time = timer.perf_counter()
    nw = greedy_3_tree.Greedy3Tree(nw)
    end_time = timer.perf_counter()
    print("\n--------------- Greedy 3 Tree Heuristic stats ---------------\n")
    print("Execution time: ", end_time - start_time, "seconds.")
    print("Is network connected: ", nw.is_network_connected())
    print("Is Network connectivity 3:", nw.check_network_connectivity(3))
    print("Network diameter: ", nw.check_network_diameter())
    # print("Network node eccentricity", nw.check_node_eccentricity())
    print("Total network cost: ", nw.get_total_network_cost())
    nw.draw_network()

    # DescendingTree run
    # Re-initialize network with previous coordinates
    nw.reinitialize_network()
    start_time = timer.perf_counter()
    nw = descending_tree.DescendingTree(nw)
    end_time = timer.perf_counter()
    print("\n-------------- Descending Tree Heuristic stats --------------\n")
    print("Execution time: ", end_time - start_time, "seconds.")
    print("Is network connected: ", nw.is_network_connected())
    print("Is Network connectivity 3", nw.check_network_connectivity(3))
    print("Network diameter: ", nw.check_network_diameter())
    # print("Network node eccentricity", nw.check_node_eccentricity())
    print("Total network cost: ", nw.get_total_network_cost())
    nw.draw_network()


if __name__ == "__main__":
    start(sys.argv)
