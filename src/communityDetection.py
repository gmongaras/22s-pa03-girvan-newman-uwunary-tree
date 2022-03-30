from networkx import graphml
import networkx as nx
from collections import deque
import numpy as np
import random
from collections import deque



# Parameters
inFile = "../data/dataset.graphml"  # The datafile to load in
nodeSubsetPercent = 0.1             # Number of random nodes to pick in the betweeness algorithm
        




# Inputs:
#   G - The graph to calculate
# Output
#   edges - The betweeness between all edges
# def calculateBetweeness(G, paths, removedEdges, edges):
#     # Calculate the number of nodes to sample
#     nodes = list(G.nodes)
#     numNodes = len(nodes)
#     nodeSubsetSize = int(nodeSubsetPercent*numNodes)
    
#     # Select a specified percent of nodes to look at
#     #random.shuffle(nodes)
#     #selectedNodes = nodes[:nodeSubsetSize]
    
    
#     # If the removed edge is empty, calculate all paths
#     if removedEdges == None:
#         # Create a dictionary of edges
#         edges = {i:0 for i in list(G.edges)}
        
#         # Iterate over all selected nodes
#         for n1 in range(0, numNodes):
#             # Iterate over all nodes that haven't been visited
#             for n2 in range(n1+1, numNodes):
#                 # Find the shortest paths between the nodes if it exists
#                 try:
#                     shortestPaths = list(nx.all_shortest_paths(G, nodes[n1], nodes[n2]))
#                 # If no path exists, skip to the next node
#                 except nx.NetworkXNoPath:
#                     continue
                
#                 # New edges to add to the total edge counts
#                 newEdges = dict()
#                 for path in shortestPaths:
#                     for i in range(0, len(path)-1):
#                         try: # Does the key exist
#                             newEdges[(path[i], path[i+1])] += 1
#                         except KeyError:
#                             newEdges[(path[i], path[i+1])] = 1
                
#                 # Add all edges to the total edge counts as an inverse
#                 # of the current value to compensate for multiple paths
#                 for k in newEdges.keys():
#                     try: # Should the 0 and 1 indices be flipped?
#                         edges[(k[0], k[1])] += 1/float(newEdges[k])
#                     except KeyError:
#                         edges[(k[1], k[0])] += 1/float(newEdges[k])
                
#                 # Add the paths to the paths dict
#                 for path in shortestPaths:
#                     # Iterate over each path and add each edge, path
#                     # combination to the paths dict
#                     for i in range(0, len(path)-1):
#                         try: # Does paths have the key already?
#                             paths[(path[i], path[i+1])].append((path, 1/float(newEdges[(path[i], path[i+1])])))
#                         except KeyError:
#                             try: # Swap the order of i and i+1 if needed
#                                 paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i], path[i+1])]))]
#                             except KeyError:
#                                 paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i+1], path[i])]))]
    
#     # If the removed edge is not None, recalculate paths for the
#     # removed edge
#     else:
#         # Iterate over all removed edges
#         for edge in removedEdges:
#             # Iterate over all paths for that edge
#             for p in paths[edge].copy():
#                 # Recalculate the path between the two nodes
                
#                 # Find the shortest paths between the nodes if it exists
#                 try:
#                     shortestPaths = list(nx.all_shortest_paths(G, p[0][0], p[0][-1]))
#                 # If no path exists, skip to the next node
#                 except nx.NetworkXNoPath:
#                     continue
                
#                 # New edges to add to the total edge counts
#                 newEdges = dict()
#                 for path in shortestPaths:
#                     for i in range(0, len(path)-1):
#                         try: # Does the key exist
#                             newEdges[(path[i], path[i+1])] += 1
#                         except KeyError:
#                             newEdges[(path[i], path[i+1])] = 1
                
#                 # Add all edges to the total edge counts as an inverse
#                 # of the current value to compensate for multiple paths
#                 for k in newEdges.keys():
#                     try: # Should the 0 and 1 indices be flipped?
#                         edges[(k[0], k[1])] += 1/float(newEdges[k])
#                     except KeyError:
#                         edges[(k[1], k[0])] += 1/float(newEdges[k])
                
#                 # Add the paths to the paths dict
#                 for path in shortestPaths:
#                     # Iterate over each path and add each edge, path
#                     # combination to the paths dict
#                     for i in range(0, len(path)-1):
#                         try: # Does paths have the key already?
#                             paths[(path[i], path[i+1])].append((path, 1/float(newEdges[(path[i], path[i+1])])))
#                         except KeyError:
#                             try: # Swap the order of i and i+1 if needed
#                                 paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i], path[i+1])]))]
#                             except KeyError:
#                                 paths[(path[i], path[i+1])] = [(path, 1/float(newEdges[(path[i+1], path[i])]))]
        
#     # return the betweeness and the updated paths
#     return edges, paths
    
    
    
class Node:
    # Initialze the node
    # Input:
    #   value - The value of the node
    #   level - The level of the node in the tree 
    def __init__(self, value, level):
        self.val = value        # Value stored in the node
        self.shortestPaths = 1  # The number of shortest paths that can
                                # reach this node from the root
        self.children = []      # Children of this node
        self.parents = []       # The parents of this node
        self.sameLevel = []     # Nodes on same level as this one
        self.level = level      # The level of the node
    
    # Test if two nodes are equal
    # Inputs:
    #   n - A node to test against this node
    def __eq__(self, n):
        return n.val == self.val
    
    # Add a child to this node
    # Input:
    #   c - A child node to add to this node
    def addChild(self, c):
        self.children.append(c)
        c.parents.append(self)
    
    # Add a parent to this node
    # Input:
    #   p - The parent to add to this node
    def addParent(self, p):
        self.parents.append(p)
        p.children.append(self)
        self.shortestPaths += 1
        
    # True if the given node is a child of this node, false otherwise
    # Inputs:
    #   n - A node to look for in this node's children
    def isChild(self, n):
        return n in self.c



# Inputs:
#   node - A node of the tree of the graph in tree form
#   parent - The parent of the given node to examine
#   edges - A dictionary of edges to add edges to
# Output:
#   None (edges is changed in the function)
def edgeLabelling(node, parent, edges):
    # If node is a root node, iterate to the child nodes and
    # calculate their betweeness
    
    # If node is a leaf, calculate the betweeness of
    # the edges between it and it's parent
    if len(node.children) == 0:
        # If the node has multiple parents, divide the
        # betweeness value
        betweeness = 1/float(len(node.parents))
        
        
        
        ## Store the betweeness
        
        try: # Does the key (parent, child) exist?
            edges[(parent.val, node.val)] += betweeness
        except KeyError:
            try: # Does the key (child, parent) exist?
                edges[(node.val, parent.val)] += betweeness
            except KeyError:
                # Add the key (parent, child)
                edges[(parent.val, node.val)] = betweeness
    
    # If the node is not a leaf node
    else:
        # Calculate the betweness of all its children
        for c in node.children:
            edgeLabelling(c, node, edges)
        
        # The betweeness is equal to 1 plus the edges of its children
        betweeness = 1
        for c in node.children:
            try: # Does the key (node, child) exist?
                betweeness += edges[(node.val, c.val)]
            except KeyError:
                try: # Does the key (child, node) exist?
                    betweeness += edges[(c.val, node.val)]
                except KeyError:
                    # If the key does not exist, raise an error
                    raise RuntimeError("Key must exist")
        
        # Update the shortestPaths value of the node
        node.shortestPaths = betweeness
        
        # Divide the betweeness between the parent nodes
        betweeness /= float(len(node.parents))
        
        # Store the betweeness of this node and its parent
        try: # Does the key (parent, child) exist?
            edges[(parent.val, node.val)] += betweeness
        except KeyError:
            try: # Does the key (child, parent) exist?
                edges[(node.val, parent.val)] += betweeness
            except KeyError:
                # Add the key (parent, child)
                edges[(parent.val, node.val)] = betweeness



# Inputs:
#   G - The graph to use
#   n - The node to find all paths from
#   edges - A dictionary of edges to add edges to
# Output:
#   None (edges is changed in the function)
def single_source_shortest_path(G, n, edges):
    # The visited nodes
    visited = []
    
    # Initialize the tree to the root node
    tree = Node(n, 1)
    
    
    
    
    ### Step 1 and 2 - Breadth First Search and Node Labelling
    
    # Queue used for BFS
    q = deque()
    
    # Enqueue the root node
    q.append(tree)
    visited.append(tree)
    
    # BFS variables
    curNode = tree.val  # Stores the current node being examined
    subTree = tree      # Subtree of the entire tree used to add more nodes
    level = 1           # The current level of the tree
    
    # Iterate until the queue is empty
    while q:
        # Dequeue the queue
        cur = q.pop()
        
        # The current level is the level of the current node + 1
        level = cur.level + 1
        
        # Iterate over all nodes adjacent to this node
        for n in list(G.neighbors(cur.val)):
            
            node = Node(n, level)
            try:
                # Try to get the index of the node
                # in the visited list
                loc = visited.index(node)
                
                # Get the node
                node = visited[loc]
                
                # If this node is equal to the level of cur,
                # set them as equal levels
                if node.level == cur.level:
                    if cur not in node.sameLevel:
                        node.sameLevel.append(cur)
                        cur.sameLevel.append(node)
                # If this node has a smaller level than the current
                # node, set this node as the parent of the current node
                elif node.level < cur.level:
                    if node not in cur.parents:
                        cur.addParent(node)
                
            
            # If the node isn't visited, enqueue it and add
            # it to the tree
            except ValueError:
                q.append(node)
                visited.append(node)
                cur.addChild(node)
    
    
    
    
    ### Step 3 - edge labelling
    
    # Iterate over all children of the root node
    bet = dict()
    for c in tree.children:
        edgeLabelling(c, tree, bet)
    
    # Add the betweeness to the total edges dictionary
    for edge in bet.keys():
        try: # Does the edge exist?
            edges[edge] += bet[edge]
        except KeyError:
            try: # Does the reverse of the edge exist?
                edges[(edge[1], edge[0])] += bet[edge]
            except KeyError:
                # If the edge does not exist, add it
                edges[edge] = bet[edge]
    
    # Return the edges
    return edges



# Inputs:
#   G - The graph to use
# Output
#   edges - The betweeness between all edges
def calculateBetweeness(G):
    # The betweeness of the graph
    # map:   edge -> betweeness
    betweeness = dict()
    
    # Iterate over all nodes
    for n in list(G.nodes):
        # Calculate the betweeness for all paths from that node
        #bet = nx.single_source_shortest_path(G, n)
        single_source_shortest_path(G, n, betweeness)
        
        # # Store the betweeness
        # for edge in bet.keys():
        #     # Does the edge exist in thedictionary?
        #     try:
        #         betweeness[edge] += bet[edge]
        #     except:
        #         betweeness[edge] = bet[edge]
    
    # Return the betweeness
    return betweeness
                




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
        betweeness2 = nx.edge_betweenness_centrality(G)
        betweeness = calculateBetweeness(G)
        
        # Get the edge with the max betweeness
        maxBetweeness = np.argwhere(np.array(list(betweeness.values()), dtype=np.float16) == max(np.array(list(betweeness.values()), dtype=np.float16)))
        maxBetweeness2 = np.argwhere(np.array(list(betweeness2.values()), dtype=np.float16) == max(np.array(list(betweeness2.values()), dtype=np.float16)))
        
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