from networkx import graphml
import networkx as nx
from collections import deque
import numpy as np
import random
import math
import random
import matplotlib.pyplot as plt

# Machine Learning
from model import network
from sklearn.cluster import KMeans
import yaml
import torch





# All Script Parameters
mode = "NN"                         # Mode to evaluate the graph, use NN for neural network
                                    # and "GN" (or anything else) for normal Q function.
commName = "community"              # The name of the community label in the graphml file
inFile = "../data/dataset1.graphml" # The datafile to load in

# Neural Network Parameters
configFileName = "./networkParams.yml"  # The configuration file for the model
modelFileName = "../models/512,1024,512"# The saved model to load in
numClasses = 4                          # Number of classes to predict

# Girvan Newman Parameters
nodeSubsetPercent = 0.8             # Percent of random nodes to pick in the betweeness algorithm
    
    
    
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
        self.labeled = False    # Has the node been visited in BFS?
    
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
    if node.labeled == True:
        # Divide the betweeness between the parent nodes
        if len(node.children) == 0:
            betweeness = 1/float(len(node.parents))
        else:
            betweeness = node.shortestPaths/float(len(node.parents))
        
        # Store the betweeness of this node and its parent
        try: # Does the key (parent, child) exist?
            edges[(parent.val, node.val)] += betweeness
        except KeyError:
            try: # Does the key (child, parent) exist?
                edges[(node.val, parent.val)] += betweeness
            except KeyError:
                # Add the key (parent, child)
                edges[(parent.val, node.val)] = betweeness
        return
    
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
    
    # Label the node as visited
    node.labeled = True



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
    
    # Stack used for BFS
    s = deque()
    
    # push the root node
    s.append(tree)
    visited.append(tree)
    
    # BFS variables
    level = 1           # The current level of the tree
    
    # Iterate until the queue is empty
    while s:
        # Dequeue the stack
        cur = s.pop()
        
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
                
            
            # If the node isn't visited, push it and add
            # it to the tree
            except ValueError:
                s.append(node)
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
            edges[edge] += bet[edge]/2
        except KeyError:
            try: # Does the reverse of the edge exist?
                edges[(edge[1], edge[0])] += bet[edge]/2
            except KeyError:
                # If the edge does not exist, add it
                edges[edge] = bet[edge]/2
    
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
    
    # Get a subset of the graph
    e = list(G.edges)
    random.shuffle(e)
    sub = G.edge_subgraph(e[:int(len(e)*nodeSubsetPercent)])
    
    # Iterate over all nodes
    for n in list(sub.nodes):
        # Calculate the betweeness for all paths from that node
        single_source_shortest_path(sub, n, betweeness)
    
    # Return the betweeness
    return betweeness




# Input:
#   G - The graph to iterate
#   node - The node to look at in the graph
#   visited - The already visited nodes
def findCommunities(G, node, visited):
    # Iterate over all nodes adjacent to this node
    # and add them to the visited nodes
    for n in list(G.neighbors(node)):
        # If the node hasn't been visited, add it
        # to the community and visit its neighbors
        if n not in visited:
            visited.append(n)
            findCommunities(G, n, visited)
                




# Use the normal Q value to stop the loop when removing
# edges from the graph
# Inputs:
#   G - The graph to remove edges from
# Outputs:
#   G - New graph with edges removed
def normalLoop(G):
    # Iterate until the Q value is no longer increasing
    Q_prev = -np.inf
    Q = -np.inf
    maxBetweeness = [0]
    iter = 1
    while (Q+0.05 >= Q_prev):#len(G.edges) and len(maxBetweeness) > 0):
        # Update the Q_prev value
        Q_prev = Q
        
        # Calculate the betweeness of all edges in the graph
        betweeness = calculateBetweeness(G)
        
        # If the betweeness is empty, break the loop
        if len(betweeness.keys()) == 0:
            break
        
        # Get the edges with the max betweeness
        a = list(betweeness.values())[np.argmax(np.array(list(betweeness.values()), dtype=np.float16))]
        maxBetweeness = np.argwhere(np.array(list(betweeness.values()), dtype=np.float16) >= a/2)
        
        # Store the number of edges before removing any edges (m)
        m = len(list(G.edges))
        
        # Store the old graph
        oldG = G.copy()
        
        # Remove all max edges from the graph
        for edge in maxBetweeness:
            e = list(betweeness.keys())[edge.item()]
            G.remove_edge(e[0], e[1])
        
        print(f"Iters: {iter},  Removes: {len(maxBetweeness)}")
        
        
        
        
        
        ### Compute the modularity (Q)
        # https://www.pnas.org/doi/full/10.1073/pnas.0601602103#FD3
        
        # - B_ij = (A - (k_i-k_j)/2m)
        #    - A_ij = Number of edges between node i and j
        #    - k_i = degree of node i
        #    - k_j = degree of node j
        #    - m = number of edges in the old graph
        # - s_i * s_j = 1 if i and j are in the same group, -1 otherwise
        # - sum1 = The first summation
        #    - sum_ij[ B_ij*(s_i*s_j +1) ]
        # - sum2 = The second summation
        #    - sum_ij[ B_ij ]
        
        # Iterate over all nodes in the old graph (i)
        sum1 = 0
        sum2 = 0
        
        # Iterate over all nodes in the old graph
        for i in list(oldG.nodes):
            
            # Get the neightbors for node i in the graph
            neighbors_i = list(G.neighbors(i))
            k_i = len(neighbors_i)
            
            # Get the communities in the current graph for node i
            comm = []
            findCommunities(G, i, comm)
            
            # Iterate over all nodes in the new graph (j)
            for j in list(G.nodes):
                ## Calculate the B value
                
                # Get the neighbors for node j
                neighbors_j = list(G.neighbors(j))
                k_j = len(neighbors_j)
                
                # Get the number of edges between node i and node j
                A_ij = 1 if ((i, j) in G.edges or (j, i) in G.edges) else 0
                
                # Calculate the final B value
                B = A_ij - (k_i*k_j)/(2*m)
                
                
                # Calculate the s value (s_i * s_j) + 1
                s = 1 if j in comm else -1
                s += 1
                
                # Compute the B values to be summed
                B_1 = B*s
                B_2 = B
                
                # Store the B values
                sum1 += B_1
                sum2 += B_2
        
        # Compute the final Q value
        Q = (1/(2*m))*(0.5*sum1 - sum2)
        
        print(f"Iter {iter} Modularity: {Q}")
        iter += 1
    
    # We want the graph from the itertion before the last since the last
    # iteration ended with a lower Q score
    G = oldG
    
    return G



# Use a neural network to get the communities from the graph
# Inputs:
#   G - The graph to remove edges from
# Outputs:
#   comm - The calssified nodes in the graph
def neuralNetworkLoop(G):
    # Load the configuration file
    with open(configFileName) as ymlFile:
        cfg = yaml.safe_load(ymlFile)

    # Save the info from the file
    inDim = cfg["inDim"]
    EncoderInfo = cfg["Encoder"]
    DecoderInfo = cfg["Decoder"]
    
    # Ensure the inDim has the same number of nodes as the graph
    assert inDim == len(list(G.nodes)), f"Network needs to have an input dimension with the same size as the number of nodes in the graph. Network Dim = {inDim}. Graph Nodes = {len(list(G.nodes))}"

    # Create the network
    model = network(inDim, EncoderInfo, DecoderInfo)
    
    # Load in the model
    model.loadModel(modelFileName)
    
    
    
    
    
    ### Compute the B value
    # - B_ij = (A - (k_i-k_j)/2m)
    #    - A_ij = Number of edges between node i and j
    #    - k_i = degree of node i
    #    - k_j = degree of node j
    #    - m = number of edges in the old graph
    
    # The B matrix
    B_ij = []
    
    # Calculate the m value
    m = len(list(G.edges))
    
    # Get the list of nodes
    nodes = list(G.nodes)
    
    # Iterate over all nodes in the old graph (i)
    for i in nodes:
        neighbors_i = list(G.neighbors(i))
        k_i = len(neighbors_i)
        
        # B vector for node i
        B_i = []
        
        # Iterate over all nodes in the new graph (j)
        for j in nodes:
            # Calculate the B value
            neighbors_j = list(G.neighbors(j))
            k_j = len(neighbors_j)
            #A_ij = 1 if ((i, j) in G.edges or (j, i) in G.edges) else 0
            A_ij = len(list(set(neighbors_i) & set(neighbors_j)))
            
            B = A_ij - (k_i*k_j)/(2*m)
        
            # Add the value to the B vector
            B_i.append(B)
        
        # Add the vector to the B matrix
        B_ij.append(B_i)
    
    
    
    
    # Get the prediction from the model on the B value
    H, M = model(torch.tensor(B_ij))
    H = H.cpu().detach().numpy()
    
    # Classify the nodes
    classes = KMeans(n_clusters=numClasses).fit(H).labels_
    
    # Classify each node
    comm = {i:[] for i in range(0, numClasses)}
    for i in range(0, len(classes)):
        comm[classes[i]].append(nodes[i])
        
    # Create a list from the dictionary
    comm = [i for i in comm.values()]
    
    
    # Return the classified nodes
    return comm



# Calculate the accuracy of a graph given the labelled nodes of
# a graph and the actual labels for each node
# Inputs:
#   X - The predicted labels of the nodes in the graph
#   y - The actual labels of the nodes in the graph
def calculateAccuracy(X, y):
    correct = 0                     # Number of nodes classified correctly
    
    # Calculate the total number of nodes in the graph
    total = 0
    for i in X:
        total += len(i)
    
    # Iterate through all communities in X
    for xComm in X:
        ## Find the y community that matches most with the X community.
        ## The best one has the greatest intersection
        best = None     # The best group match
        bestIdx = None  # Index in y of the best match
        bestScore = 0   # The best number of nodes that match between the groups
        
        # Iterate over all communities in y
        for yComm_idx in range(0, len(y)):
            yComm = y[yComm_idx]
            
            # Get the intersection of the two lists
            intersection = list(set(xComm) & set(yComm))
            
            # Store the y list if it matches better than the rest
            if len(intersection) > bestScore:
                best = yComm
                bestIdx = yComm_idx
                bestScore = len(intersection)
        
        
        # If there is a best score, update the accumulators
        if bestScore > 0:
            # Update the number of nodes that were classified correctly
            correct += bestScore
            
            # Remove the y community from the labels
            del y[bestIdx]
            
            # Stop the loop if there are no more nodes in y
            if len(y) == 0:
                break
    
    # Calculate the accuracy
    accuracy = float(correct)/float(total)
    
    return accuracy
            



def main():
    # Read in the graph and store data on it
    G = graphml.read_graphml(inFile)
    orig = G.copy()
    
    # Remove edges from the graph to get the communities
    if mode == "NN":
        comm = neuralNetworkLoop(G)
    else:
        G = normalLoop(G)
        
        # Iterate over all nodes and find the communities
        comm = []           # The communities found
        totalVisited = []   # The total visited nodes
        for node in list(G.nodes):
            # If the node has been visited, skip this iteration
            if node in totalVisited:
                continue
        
            visited = []    # The nodes that were visited already
            findCommunities(G, node, visited)
            
            # Add the visited nodes to the communities
            if len(visited) != 0:
                comm.append(visited)
            else:
                comm.append([node])
            
            # Add the visited nodes to the total visited nodes
            totalVisited += visited
    
    ### Graphing
    
    # Put all the leftover nodes (nodes without a class)
    # into the same class
    leftovers = []
    for c in range(0, len(comm)):
        if len(comm[c]) == 1:
            leftovers.append(comm[c][0])
    
    # Store the leftovers in the main list
    for l in range(0, len(leftovers)):
        comm.remove([leftovers[l]])
    if len(leftovers) > 0:
        comm.append(leftovers)
    
    # Get some random colors to classify every node
    vals = "123456789ABCDEF"
    colors = dict()
    for i in range(0, len(comm)):
        colors[i] = "#"+"".join([random.choice(vals) for j in range(0, 6)])
    
    # Color each node
    color_map = []
    for node in G:
        group = 0
        for g in range(0, len(comm)):
            if node in comm[g]:
                group = g
                break
        color_map.append(colors[group])
    
    # Create the graph
    nx.draw(orig, node_color=color_map, with_labels=True)
    plt.show()
    
    # Print the classes
    print("\n\n")
    for c in range(0, len(comm)):
        print(f"Class {c}: ", end="")
        for v in comm[c][:-1]:
            print(v, end=", ")
        print(comm[c][-1])
        
    # Get the communities for each node
    y_communities = dict()
    for n in orig._node.keys():
        try:
            y_communities[orig._node[n][commName]].append(n)
        except KeyError:
            y_communities[orig._node[n][commName]] = [n]
    
    # Convert the dictionary to a list
    y = [i for i in y_communities.values()]
    
    # Calculate the accuracy
    acc = calculateAccuracy(comm, y)
    
    # Display the accuracy
    print(f"Accuracy: {acc}")



if __name__ == '__main__':
    main()