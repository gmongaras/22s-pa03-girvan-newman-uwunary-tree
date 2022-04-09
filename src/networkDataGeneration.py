import networkx as nx
import random
import numpy as np
import os

# Note: Change These Parameters to Configure as Discussed in the Readme

# Parameters
dirName = "../networkTrainData"  # Directory to save arrays to
numNodes = 128  # Number of nodes in the graph
percentFunc = lambda: random.uniform(0.01, 0.6)  # Function to get random percent
numGraphs = 1000  # Number of graphs to generate

# Create Graph Object
G = nx.Graph()

# Add numNodes Number of Nodes to Graph
for n in range(0, numNodes):
    G.add_node(n)

# Get List of all Possible Edges in Graph
edges = []
for n1 in range(0, numNodes):
    for n2 in range(0, numNodes):
        if n1 != n2:
            edges.append((n1, n2))
numEdges = len(edges)

# Generate numGraphs Number of Graphs
for g in range(0, numGraphs):

    # Open File to Write to
    file = open(os.path.join(dirName, str(g)+".npy"), "wb")
    
    # Get Number of Edges
    numEdges_sample = int(percentFunc()*numEdges)
    
    # Get Subset of Edges
    random.shuffle(edges)
    sub = edges[:numEdges_sample]
    
    # Create Copy of Graph
    Gcp = G.copy()
    
    # Add Edges to Copied Graph
    Gcp.add_edges_from(sub)
    
    # B Matrix
    B = []
    
    # Calculate m Value
    m = len(list(Gcp.edges()))
    
    # Iterate over Nodes in Old Graph (i)
    for i in list(Gcp.nodes):
        neighbors_i = list(Gcp.neighbors(i))
        k_i = len(neighbors_i)

        # B Vector
        B_i = []
        
        # Iterate over Nodes in New Graph (j)
        for j in list(Gcp.nodes):

            # Calculate B Value
            neighbors_j = list(Gcp.neighbors(j))
            k_j = len(neighbors_j)
            A_ij = 1 if ((i, j) in Gcp.edges or (j, i) in Gcp.edges) else 0

            # Calculating B
            B_ij = A_ij - (k_i * k_j) / (2 * m)
        
            # Add Value to B Vector
            B_i.append(B_ij)
        
        # Add Vector to B Matrix
        B.append(B_i)
    
    # Save B Matrix to File
    np.save(file, B, allow_pickle=False)
