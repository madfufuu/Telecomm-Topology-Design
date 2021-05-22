# Telecommunication Topology Design Problem

### Project Files
    driver.py
    descending_tree.py
    greedy_3_tree.py
    network.py
    utils.py
### Project Dependencies
  * Python 3.8.8
  * Numpy
  * Matplotlib
  * NetworkX 2.5
### Description
Given the location of n nodes in a 2 dimension plane. Design a heuristic algorithm to find a sufficiently optimal network topology such that it contains the following properties:

1. The network topology contains all given nodes, therefore the network topology must be a connected network
2. The degree of each vertex in the graph is at least 3, that is, each node is connected to at least 3 other nodes
3. The diameter of the graph is at most 4. Meaning for any node i could reach any other node in the network by at most 4 hops
4. Minimize the total cost of the network topology

### Usage
    python driver.py <n>

Where n is the number of nodes to be initialized in network [15, 100].

### Heuristic Algorithms
The project contains two heuristic algorithms that solves the Telecommunication Topology Design Problem:
#### <i><u>Greedy 3 Tree</u></i>

As the name suggests, the idea behind this algorithm is to essentially divide up the nodes in the network into groups of 3. There are a couple of benefits of doing this:
1. Simplicity. By localizing the nodes into smaller subsets, we’re basically breaking up the problem into smaller, and more-trivial cases. It enables the algorithm to better keep track of the conditions needed for each subset with more simplicity.
2. Efficiency. This technique inherits some of the properties of divide and conquer algorithm. By splitting up the problem and combining partial solutions to form the final topology, we limit the number of sub-problems of size to around n/p; which greatly reduces the time complexity and space complexity needed to solve a more difficult problem.
3. Better control over algorithm. By dividing up the nodes, we have much more control of each subgroup’s heuristic and performance. This could help us easily modify the heuristic’s parameters and stages of the algorithm; or just in general help us better debug the program.

A few hypotheses was stated before implementing the algorithm and then verified the heuristics behind the algorithm, here are some of the observations and behaviors of the network.

* Any sub-trees in groups of 5 or less nodes have a diameter of 4 or less; as the number of nodes in sub-trees grow with to 6 or more, the sub-tree’s diameter may no longer hold the property of a minimal of 4 in network diameter. This is the case when the sub-tree formation occurs where the disjoint nodes are connected in a linear slope.
* When joining sub-trees with size 2 or larger, we can no longer guarantee the product sub-tree retains the properties of the smaller subtrees.
* As the number of nodes in sub-trees grow, more nodes needs to be connected in order to maintain the desired properties in the final tree.

After verifying these behaviors of sub-trees and experimenting with different size of sub-trees, decision was made to initialize the network with sub-trees of size 3 because it was the most consistent with expected behaviors to maintain diameter constraint without sacrificing too much efficiency. The core behind this heuristic algorithm relies on a very important property of 3-connected sub-trees:

The result of joining two 3-connected sub-trees retains the diameter property if the middle node is used to connect to the other tree.

The number of connections needed to join 6-connected sub-trees and 12-connected sub-trees grows as a function:

    𝒇(𝒙) = 𝟐^𝒏 𝒘𝒉𝒆𝒓𝒆 𝒏 𝒊𝒔 𝒕𝒉𝒆 𝒏𝒖𝒎𝒃𝒆𝒓 𝒐𝒇 𝒎𝒊𝒅 𝒏𝒐𝒅𝒆𝒔 𝒑𝒓𝒆𝒔𝒆𝒏𝒕 𝒊𝒏 𝒕𝒉𝒆 𝒕𝒓𝒆𝒆

The Greedy 3 Tree algorithm takes advantage of properties of 3-connected sub-trees and utilizes the middle-points in these sub-trees to maintain diameter of the connected nodes. After forming 12-connected sub-trees, we take a step towards completing the degree requirements for any nodes that does not have at least 3 degrees. The resulting network topology will therefore retain the property constraints of the smaller sub-trees.

#### <i><u>Descending Tree</u></i>

This is a different approach with similarities to the Greedy 3 Tree algorithm and references to using the greedy algorithm in a more brute-force way. The main difference of this algorithm compared to Greedy 3 Tree is that the initialized network topology is a Complete Graph representation of all the nodes, we take steps in reducing the total-cost and removing edges based on a greedy approach, hence the name Descending Tree.

The Descending Tree algorithm takes advantage of properties of a Complete Graph, where every node is connected to every other node in the graph, meaning we have satisfied the degree and diameter constraints of the network in the beginning, but have intentionally omitted minimizing the topology. 
This approach simplifies the problems by trying to maintain the satisfied constraints on the network throughout its iterations on all of the edges, while the obvious downside to this is efficiency and the inability to recognize more optimal edges that are too long, it could be solved with random-walk and the application of a greedy flip.

The Descending Tree algorithm attempts to remove the longest length edge from the network like a stack, if the removal of an edge invalidates the constraints of the network, we simply add it back into the network and try to remove the next longest edge.
