from networkx import graphml
import networkx as nx
from collections import deque
import numpy as np
import random



# Parameters
inFile = "../data/dataset.graphml"  # The datafile to load in
nodeSubsetPercent = 0.1             # Number of random nodes to pick in the betweeness algorithm
        




# Inputs:
#   G - The graph to calculate
# Output
#   edges - The betweeness between all edges
def calculateBetweeness(G, paths, removedNode):
    # Calculate the number of nodes to sample
    nodes = list(G.nodes)
    numNodes = len(nodes)
    nodeSubsetSize = int(nodeSubsetPercent*numNodes)
    
    # Create a dictionary of edges
    edges = {i:0 for i in list(G.edges)}
    
    # Select a specified percent of nodes to look at
    #random.shuffle(nodes)
    #selectedNodes = nodes[:nodeSubsetSize]
    
    
    # If the removed node is empty, calculate all paths
    if len(paths.keys()) == 0:
        # Iterate over all selected nodes
        for n1 in range(0, numNodes):
            # Iterate over all nodes that haven't been visited
            for n2 in range(n1+1, numNodes):
                # Find the shortest paths between the nodes if it exists
                try:
                    shortestPaths = list(nx.all_shortest_paths(G, nodes[n1], nodes[n2]))
                # If no path exists, skip to the next node
                except nx.NetworkXNoPath:
                    continue
                
                # New edges to add to the total edge counts
                newEdges = dict()
                for path in shortestPaths:
                    for i in range(0, len(path)-1):
                        try:
                            newEdges[(path[i], path[i+1])] += 1
                        except KeyError:
                            newEdges[(path[i], path[i+1])] = 1
                
                # Add all edges to the total edge counts as an inverse
                # of the current value to compensate for multiple paths
                for k in newEdges.keys():
                    try:
                        edges[k] += 1/float(newEdges[k])
                    except KeyError:
                        edges[(k[1], k[0])] += 1/float(newEdges[k])
    
    # If the removed node is not empty, recalculate paths for the
    # removed edge
        
    # return the betweeness and the updated paths
    return edges, paths
                




def main():
    # Read in the graph and store data on it
    G = graphml.read_graphml(inFile)
    
    c = list(nx.algorithms.community.centrality.girvan_newman(G, most_valuable_edge=None))
    
    # edges and paths that go through them
    paths = dict()
    
    # Iterate until the number of edges is 0
    while (len(G.edges) > 0):
        
        # Calculate the betweeness of all edges in the graph
        betweeness, paths = calculateBetweeness(G, paths)
        
        # Get the node with the max betweneess
        maxBetweeness = np.argwhere(np.array(list(betweeness.values()), dtype=np.float16) == max(np.array(list(betweeness.values()), dtype=np.float16)))

        # Remove the edges with the max betweeness
        for val in maxBetweeness:
            maxEdge = list(betweeness.keys())[val.item()]
            G.remove_edge(maxEdge[0], maxEdge[1])
        print(len(G.edges))
    
    print()



main()