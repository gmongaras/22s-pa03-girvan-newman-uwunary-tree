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
def calculateBetweeness(G, paths, removedEdges, edges):
    # Calculate the number of nodes to sample
    nodes = list(G.nodes)
    numNodes = len(nodes)
    nodeSubsetSize = int(nodeSubsetPercent*numNodes)
    
    # Select a specified percent of nodes to look at
    #random.shuffle(nodes)
    #selectedNodes = nodes[:nodeSubsetSize]
    
    
    # If the removed edge is empty, calculate all paths
    if removedEdges == None:
        # Create a dictionary of edges
        edges = {i:0 for i in list(G.edges)}
        
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
                        try: # Does the key exist
                            newEdges[(path[i], path[i+1])] += 1
                        except KeyError:
                            newEdges[(path[i], path[i+1])] = 1
                
                # Add all edges to the total edge counts as an inverse
                # of the current value to compensate for multiple paths
                for k in newEdges.keys():
                    try: # Should the 0 and 1 indices be flipped?
                        edges[(k[0], k[1])] += 1/float(newEdges[k])
                    except KeyError:
                        edges[(k[1], k[0])] += 1/float(newEdges[k])
                
                # Add the paths to the paths dict
                for path in shortestPaths:
                    # Iterate over each path and add each edge, path
                    # combination to the paths dict
                    for i in range(0, len(path)-1):
                        try: # Does paths have the key already?
                            paths[(path[i], path[i+1])].append((path, 1/float(newEdges[(path[i], path[i+1])])))
                        except KeyError:
                            try: # Swap the order of i and i+1 if needed
                                paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i], path[i+1])]))]
                            except KeyError:
                                paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i+1], path[i])]))]
    
    # If the removed edge is not None, recalculate paths for the
    # removed edge
    else:
        # Iterate over all removed edges
        for edge in removedEdges:
            # Iterate over all paths for that edge
            for p in paths[edge].copy():
                # Recalculate the path between the two nodes
                
                # Find the shortest paths between the nodes if it exists
                try:
                    shortestPaths = list(nx.all_shortest_paths(G, p[0][0], p[0][-1]))
                # If no path exists, skip to the next node
                except nx.NetworkXNoPath:
                    continue
                
                # New edges to add to the total edge counts
                newEdges = dict()
                for path in shortestPaths:
                    for i in range(0, len(path)-1):
                        try: # Does the key exist
                            newEdges[(path[i], path[i+1])] += 1
                        except KeyError:
                            newEdges[(path[i], path[i+1])] = 1
                
                # Add all edges to the total edge counts as an inverse
                # of the current value to compensate for multiple paths
                for k in newEdges.keys():
                    try: # Should the 0 and 1 indices be flipped?
                        edges[(k[0], k[1])] += 1/float(newEdges[k])
                    except KeyError:
                        edges[(k[1], k[0])] += 1/float(newEdges[k])
                
                # Add the paths to the paths dict
                for path in shortestPaths:
                    # Iterate over each path and add each edge, path
                    # combination to the paths dict
                    for i in range(0, len(path)-1):
                        try: # Does paths have the key already?
                            paths[(path[i], path[i+1])].append((path, 1/float(newEdges[(path[i], path[i+1])])))
                        except KeyError:
                            try: # Swap the order of i and i+1 if needed
                                paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i], path[i+1])]))]
                            except KeyError:
                                paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i+1], path[i])]))]
        
    # return the betweeness and the updated paths
    return edges, paths
                




def main():
    # Read in the graph and store data on it
    G = graphml.read_graphml(inFile)
    
    # edges and paths that go through them
    # paths = dict()
    # removedEdges = None
    # betweeness = None
    
    # Iterate until the number of edges is 0
    while (len(G.edges) > 0):
        
        # Calculate the betweeness of all edges in the graph
        betweeness = nx.edge_betweenness_centrality(G)
        
        # Get the edge with the max betweeness
        maxBetweeness = np.argwhere(np.array(list(betweeness.values()), dtype=np.float16) == max(np.array(list(betweeness.values()), dtype=np.float16)))
        
        # Remove all max edges from the graph
        for edge in maxBetweeness:
            e = list(betweeness.keys())[edge.item()]
            G.remove_edge(e[0], e[1])
        print(len(G.edges))
        
        # # Calculate the betweeness of all edges in the graph
        # betweeness, paths = calculateBetweeness(G, paths, removedEdges, betweeness)
        
        # # Get the edge with the max betweeness
        # maxBetweeness = np.argwhere(np.array(list(betweeness.values()), dtype=np.float16) == max(np.array(list(betweeness.values()), dtype=np.float16)))

        # # Reduce the edge betweeness for all paths that include
        # # the edges to remove
        # for val in maxBetweeness:
        #     # Get the paths
        #     maxEdge = list(betweeness.keys())[val.item()]
        #     edgePaths = paths[maxEdge]
            
            
        #     # Iterate over all paths
        #     for path in edgePaths:
        #         # Iterate over all pairs in the paths
        #         for i in range(0, len(path[0])-1):
        #             try: # Swap i and i+1 if needed
        #                 betweeness[(path[0][i], path[0][i+1])] -= path[1]
        #             except:
        #                 betweeness[(path[0][i+1], path[0][i])] -= path[1]

        # # Remove the edges with the max betweeness
        # for val in maxBetweeness:
        #     maxEdge = list(betweeness.keys())[val.item()]
        #     G.remove_edge(maxEdge[0], maxEdge[1])
        
        # print(len(G.edges))
        # removedEdges = [list(betweeness.keys())[val.item()] for val in maxBetweeness]
    
    print()



main()