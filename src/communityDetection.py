# Girvan Newman
import matplotlib.pyplot as plt
from networkx import graphml
import networkx as nx
from collections import deque
import numpy as np
import random

# Machine Learning
from model import network
from sklearn.cluster import KMeans
import yaml
import torch

# Note: Change These Parameters to Configure as Discussed in the Readme

# All Script Parameters
mode = "NN"                         # Mode to evaluate the graph, use NN for neural network
                                    # and "GN" (or anything else) for normal Q function.
commName = "community"              # The name of the community label in the graphml file
inFile = "../data/dataset1.graphml" # The datafile to load in

# Neural Network Parameters
configFileName = "./networkParams.yml"  # The configuration file for the model
modelFileName = "../models/256,128"# The saved model to load in
numClasses = 4                          # Number of classes to predict

# Girvan Newman Parameters
nodeSubsetPercent = 0.8  # Percent of Random Nodes to Pick in the Betweenness Algorithm


# Input: (To Initialize Node)
# Value = Value Stored Within Node
# Level = Level of Node
class Node:

    def __init__(self, value, level):
        self.level = level  # Level of Node
        self.val = value  # Value stored in the node
        self.shortestPaths = 1  # Number of Shortest Paths that can Reach this Node from Root
        self.children = []  # Children of Node
        self.parents = []  # Parents of Node
        self.sameLevel = []  # Nodes on Same Level
        self.labeled = False  # Has Node Been Visited in BFS?

    # Add Child to Node (Input Node)
    def addChild(self, c):
        self.children.append(c)
        c.parents.append(self)
    
    # Add Parent to Node (Input Node)
    def addParent(self, p):
        self.parents.append(p)
        p.children.append(self)
        self.shortestPaths += 1
        
    # Checks if Node is Child (Input Node)
    def isChild(self, n):
        return n in self.c

    # Tests if two Nodes are Equal (Input Node)
    def __eq__(self, n):
        return n.val == self.val


# Inputs:
# node = Node of Tree of Graph
# parent = Parent of Given Node
# edges = Dictionary of Edges
# Outputs:
# None (Edges Changed Within Function)
def edgeLabelling(node, parent, edges):

    if node.labeled:
        # Divide Betweenness of Parent Nodes
        if len(node.children) == 0:
            betweenness = 1 / float(len(node.parents))
        else:
            betweenness = node.shortestPaths / float(len(node.parents))
        
        # Store Betweenness of Node and Parent
        try:
            # Does Key (parent, child) Exist?
            edges[(parent.val, node.val)] += betweenness
        except KeyError:
            try:
                # Does Key (child, parent) Exist?
                edges[(node.val, parent.val)] += betweenness
            except KeyError:
                # Add Key (parent, child)
                edges[(parent.val, node.val)] = betweenness

        return
    
    # If Root Node, Iterate to Child Nodes and Calculate Their Betweenness
    
    # If Node is a Leaf Node, Not Labelled
    if len(node.children) == 0:
        # If Node has Multiple Parents, Divide Betweenness Value
        betweenness = 1 / float(len(node.parents))

        # Store Betweenness of Node and Parent
        try:
            # Does Key (parent, child) Exist?
            edges[(parent.val, node.val)] += betweenness
        except KeyError:
            try:
                # Does Key (child, parent) Exist?
                edges[(node.val, parent.val)] += betweenness
            except KeyError:
                # Add Key (parent, child)
                edges[(parent.val, node.val)] = betweenness
    
    # If Node isn't a Leaf Node
    else:
        # Calculate Betweenness of all Children
        for c in node.children:
            edgeLabelling(c, node, edges)
        
        # The Betweenness is Equal to 1 + Edges of its Children
        betweenness = 1
        for c in node.children:
            try:
                # Does Key (node, child) Exist?
                betweenness += edges[(node.val, c.val)]
            except KeyError:
                try:
                    # Does Key (child, node) Exist?
                    betweenness += edges[(c.val, node.val)]
                except KeyError:
                    # If Key Does Not Exist, Raise Error
                    raise RuntimeError("Key must exist")
        
        # Update shortestPaths Value of Node
        node.shortestPaths = betweenness
        
        # Divide Betweenness Between Parent Nodes
        betweenness /= float(len(node.parents))

        # Store Betweenness of Node and Parent
        try:
            # Does Key (parent, child) Exist?
            edges[(parent.val, node.val)] += betweenness
        except KeyError:
            try:
                # Does Key (child, parent) Exist?
                edges[(node.val, parent.val)] += betweenness
            except KeyError:
                # Add Key (parent, child)
                edges[(parent.val, node.val)] = betweenness
    
    # Label Node Visited
    node.labeled = True


# Inputs:
# G = Our Graph
# n = Index of Node to find Paths
# edges = Dictionary of Edges
# Outputs:
# None (Edges Changed Within Function)
def single_source_shortest_path(G, n, edges):

    # Visited Nodes, Tree Initialization
    visited = []
    tree = Node(n, 1)

    # Step 1, 2 = BFS, Node Labelling
    
    # Stack Used for BFS, Push Root Node
    s = deque()
    s.append(tree)
    visited.append(tree)

    # Current Level of Tree
    level = 1
    
    # Iterate Until Empty Stack
    while s:

        # Dequeue Stack
        cur = s.pop()
        
        # Current Level = Level + 1
        level = cur.level + 1
        
        # Iterate over all Adjacent Nodes
        for n in list(G.neighbors(cur.val)):
            
            node = Node(n, level)
            try:
                # Try to get Index of Node in Visited List
                loc = visited.index(node)
                
                # Get Node
                node = visited[loc]
                
                # If Node is Equal to Cur Level, Set Equal Level
                if node.level == cur.level:
                    if cur not in node.sameLevel:
                        node.sameLevel.append(cur)
                        cur.sameLevel.append(node)

                # If Node has Smaller Level than Current Node,
                # Set this Node as the Parent of the Current Node
                elif node.level < cur.level:
                    if node not in cur.parents:
                        cur.addParent(node)

            # If Node is Unvisited, Push
            except ValueError:
                s.append(node)
                visited.append(node)
                cur.addChild(node)

    # Step 3 = Edge Labelling
    
    # Iterate Over All Root Node Children
    bet = dict()
    for c in tree.children:
        edgeLabelling(c, tree, bet)

    # Add Betweenness to Total Edges Dictionary
    for edge in bet.keys():
        try:
            # Does the Edge Exist?
            edges[edge] += bet[edge]/2
        except KeyError:
            try:
                # Does the Reverse Exist?
                edges[(edge[1], edge[0])] += bet[edge]/2
            except KeyError:
                # Add Edge if not Existing
                edges[edge] = bet[edge]/2

    return edges


# Inputs:
# G = Our Graph
# Output
# Edges = The Betweenness of all Edges
def calculateBetweenness(G):

    # The Betweenness of Graph
    # map: edge -> betweenness
    betweenness = dict()
    
    # Get Subset of Graph
    e = list(G.edges)
    random.shuffle(e)
    sub = G.edge_subgraph(e[:int(len(e)*nodeSubsetPercent)])
    
    # Iterate Over Nodes
    for n in list(sub.nodes):
        # Calculate Betweenness for all Paths from that Node
        single_source_shortest_path(sub, n, betweenness)

    return betweenness


# Input:
# G = Our Graph
# Node = Specified Node
# Visited = Already Visited Nodes
def findCommunities(G, node, visited):

    # Iterate over all Adjacent Nodes and Add Them to Visited Nodes
    for n in list(G.neighbors(node)):

        # If Node hasn't been Visited, Add to Community and Visit Neighbors
        if n not in visited:
            visited.append(n)
            findCommunities(G, n, visited)


# Inputs:
# G = Our Graph
# Outputs:
# G = New Graph (Removed Edges)
# Use the Normal Q value to
# Stop Loop when Removing
def normalLoop(G):

    # Iterate Until Q Value isn't Increasing
    Q_prev = -np.inf
    Q = -np.inf
    maxBetweenness = [0]
    it = 1

    while Q + 0.05 >= Q_prev:  # IE (len(G.edges) and len(maxBetweenness) > 0):

        # Update Q_prev Value
        Q_prev = Q
        
        # Calculate Betweenness of All Edges in Graph
        betweenness = calculateBetweenness(G)
        
        # If Betweenness Empty, Break Loop
        if len(betweenness.keys()) == 0:
            break
        
        # Get Max Betweenness
        a = list(betweenness.values())[np.argmax(np.array(list(betweenness.values()), dtype=np.float16))]
        maxBetweenness = np.argwhere(np.array(list(betweenness.values()), dtype=np.float16) >= a/2)
        
        # Store Number of Edges Before Removing (m)
        m = len(list(G.edges))
        
        # Copy Graph
        oldG = G.copy()
        
        # Remove all Max Edges from Graph
        for edge in maxBetweenness:
            e = list(betweenness.keys())[edge.item()]
            G.remove_edge(e[0], e[1])
        
        print(f"Iters: {it},  Removes: {len(maxBetweenness)}")

        # Compute the modularity (Q)
        # See: https://www.pnas.org/doi/full/10.1073/pnas.0601602103#FD3

        # Process:
        # - B_ij = (A - (k_i - k_j) / 2m)
        #    - A_ij = Number of Edges Between Node i and j
        #    - k_i = Degree of Node i
        #    - k_j = Degree of Node j
        #    - m = Number of Edges in Old Graph
        # - s_i * s_j = 1 if i and j are in the Same Group, -1 Otherwise
        # - sum1 = The First Summation
        #    - sum_ij[ B_ij * (s_i * s_j + 1) ]
        # - sum2 = The Second Summation
        #    - sum_ij[ B_ij ]

        sum1 = 0
        sum2 = 0

        # Iterate over Nodes in Old Graph (i)
        for i in list(oldG.nodes):
            
            # Get the Neighbors of Node i
            neighbors_i = list(G.neighbors(i))
            k_i = len(neighbors_i)
            
            # Find the Communities Associated with Node
            comm = []
            findCommunities(G, i, comm)
            
            # Iterate over Nodes in New Graph (j)
            for j in list(G.nodes):

                # Calculate B Value
                
                # Get the Neighbors of Node j
                neighbors_j = list(G.neighbors(j))
                k_j = len(neighbors_j)
                
                # Find Number of Edges Between Node i and Node j
                A_ij = 1 if ((i, j) in G.edges or (j, i) in G.edges) else 0
                
                # Calculating B
                B = A_ij - (k_i * k_j) / (2 * m)

                # Calculate s Value (s_i * s_j) + 1
                s = 1 if j in comm else -1
                s += 1
                
                # Compute Final B values for Iteration
                B_1 = B*s
                B_2 = B
                
                # Sum B values
                sum1 += B_1
                sum2 += B_2
        
        # Compute the Final Q Value
        Q = (1 / (2 * m)) * (0.5 * sum1 - sum2)

        # Print Values, Increment
        print(f"Iter {iter} Modularity: {Q}")
        it += 1

    # We Want Graph from Before Iteration Before Last
    # Since the Last Iteration Ends with Lower Q Score
    G = oldG
    return G


# Use a Neural Network to get Communities from Graph
# Inputs:
# G = Our Graph
# Outputs:
# comm - Classified Nodes in Graph
def neuralNetworkLoop(G):

    # Load Configuration File
    with open(configFileName) as ymlFile:
        cfg = yaml.safe_load(ymlFile)

    # Save Info from File
    inDim = cfg["inDim"]
    EncoderInfo = cfg["Encoder"]
    DecoderInfo = cfg["Decoder"]
    
    # Ensure inDim has the Same Number of Nodes as Graph
    assert inDim == len(list(G.nodes)), f"Network needs to have an input dimension " \
                                        f"with the same size as the number of nodes in the graph. " \
                                        f"Network Dim = {inDim}. Graph Nodes = {len(list(G.nodes))}"

    # Create Network
    model = network(inDim, EncoderInfo, DecoderInfo)
    
    # Load Model
    model.loadModel(modelFileName)

    # See Process Above (NormalLoop Regular Q)

    # B Matrix
    B_ij = []
    
    # Calculate m Value
    m = len(list(G.edges))
    
    # Get Node List
    nodes = list(G.nodes)
    
    # Iterate over Nodes in Old Graph (i)
    for i in nodes:
        neighbors_i = list(G.neighbors(i))
        k_i = len(neighbors_i)
        
        # B Vector
        B_i = []
        
        # Iterate over Nodes in New Graph (j)
        for j in nodes:

            # Calculate B Value
            neighbors_j = list(G.neighbors(j))
            k_j = len(neighbors_j)

            # See Above: A_ij = 1 if ((i, j) in G.edges or (j, i) in G.edges) else 0
            A_ij = len(list(set(neighbors_i) & set(neighbors_j)))

            # Calculating B
            B = A_ij - (k_i * k_j) / (2 * m)
        
            # Add Value to B Vector
            B_i.append(B)
        
        # Add Vector to B Matrix
        B_ij.append(B_i)

    # Get Prediction from Model on the B Value
    H, M = model(torch.tensor(B_ij))
    H = H.cpu().detach().numpy()
    
    # Classify Nodes
    classes = KMeans(n_clusters=numClasses).fit(H).labels_
    
    # Classify Each Node
    comm = {i: [] for i in range(0, numClasses)}
    for i in range(0, len(classes)):
        comm[classes[i]].append(nodes[i])
        
    # Create List from Dictionary
    comm = [i for i in comm.values()]

    # Return Classified Nodes
    return comm


# Inputs:
# X = The Predicted Labels of Nodes in Graph
# Y = The Actual Labels of Nodes in Graph
# Calculate Accuracy of Graph Given Labelled Nodes and Actual Labels
def calculateAccuracy(X, y):
    correct = 0  # Number Nodes Classified Correctly
    
    # Calculate Total Number of Nodes in Graph
    total = 0
    for i in X:
        total += len(i)
    
    # Iterate Through all Communities in X
    for xComm in X:

        # Find y Community that Matches Most With the X Community (The Greatest Intersection)
        best = None  # Best Group Match
        bestIdx = None  # Index in y of Best Match
        bestScore = 0  # The Best Number of Nodes that Match Between Groups
        
        # Iterate over all Communities in y
        for yComm_idx in range(0, len(y)):
            yComm = y[yComm_idx]
            
            # Get Intersection of the Two Lists (xComm, yComm)
            intersection = list(set(xComm) & set(yComm))
            
            # Store y List if it Matches Better than Rest
            if len(intersection) > bestScore:
                best = yComm
                bestIdx = yComm_idx
                bestScore = len(intersection)

        # If There is a Best Score, Update Accumulators
        if bestScore > 0:

            # Update Number of Nodes that Were Classified Correctly
            correct += bestScore
            
            # Remove y Community From Labels
            del y[bestIdx]
            
            # Stop Loop if There are no More Nodes in y
            if len(y) == 0:
                break
    
    # Calculate Accuracy, Return
    accuracy = float(correct) / float(total)
    return accuracy
            

def main():

    # Read in Graph, Copy Graph (Store)
    G = graphml.read_graphml(inFile)
    orig = G.copy()
    
    # Remove Edges from Graph to get Communities (Choose Mode)
    if mode == "NN":
        comm = neuralNetworkLoop(G)
    else:
        G = normalLoop(G)
        
        # Iterate over Nodes and Find Communities
        comm = []  # Found Communities
        totalVisited = []  # Total Visited Nodes
        for node in list(G.nodes):

            # If Node has been Visited, Skip Iteration
            if node in totalVisited:
                continue
        
            visited = []  # Already Visited Nodes
            findCommunities(G, node, visited)
            
            # Add Visited Nodes to Communities
            if len(visited) != 0:
                comm.append(visited)
            else:
                comm.append([node])
            
            # Add Visited Nodes to Total Visited Nodes
            totalVisited += visited
    
    # Graphing
    
    # Put all Leftover Nodes (Nodes Without Class) Into Same Class
    leftovers = []
    for c in range(0, len(comm)):
        if len(comm[c]) == 1:
            leftovers.append(comm[c][0])
    
    # Store Leftovers in Main List
    for left in range(0, len(leftovers)):
        comm.remove([leftovers[left]])
    if len(leftovers) > 0:
        comm.append(leftovers)
    
    # Get Random Colors to Classify Every Node
    vals = "123456789ABCDEF"
    colors = dict()
    for i in range(0, len(comm)):
        colors[i] = "#"+"".join([random.choice(vals) for j in range(0, 6)])
    
    # Color Each Node
    color_map = []
    for node in G:
        group = 0
        for g in range(0, len(comm)):
            if node in comm[g]:
                group = g
                break
        color_map.append(colors[group])
    
    # Create Graph (Plot)
    nx.draw(orig, node_color=color_map, with_labels=True)
    plt.show()
    
    # Print the Classes
    print("\n\n")
    for c in range(0, len(comm)):
        print(f"Class {c}: ", end="")
        for v in comm[c][:-1]:
            print(v, end=", ")
        print(comm[c][-1])
        
    # Get Communities for Each Node
    y_communities = dict()
    for n in orig._node.keys():
        try:
            y_communities[orig._node[n][commName]].append(n)
        except KeyError:
            y_communities[orig._node[n][commName]] = [n]
    
    # Convert Dictionary to List
    y = [i for i in y_communities.values()]
    
    # Calculate Accuracy
    acc = calculateAccuracy(comm, y)
    
    # Display Accuracy
    print(f"Accuracy: {acc}")


if __name__ == '__main__':
    main()
