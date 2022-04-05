import networkx as nx
import random
import numpy as np
import os


# Parameters
dirName = "../networkTrainData"                  # Directory to save arrays to
numNodes = 128                                   # Number of nodes in the graph
percentFunc = lambda : random.uniform(0.01, 0.6) # Function to get random percent
numGraphs = 1000                                 # Number of graphs to generate



# Create the graph object
G = nx.Graph()

# Add numNodes number of nodes to the graph
for n in range(0, numNodes):
    G.add_node(n)


# Get a list of all possible edges in the graph
edges = []
for n1 in range(0, numNodes):
    for n2 in range(0, numNodes):
        if n1 != n2:
            edges.append((n1, n2))
numEdges = len(edges)



# Generate numGraphs number of graphs
for g in range(0, numGraphs):
    # Open the file to write to
    file = open(os.path.join(dirName, str(g)+".npy"), "wb")
    
    # Get the number of edges
    numEdges_sample = int(percentFunc()*numEdges)
    
    # Get a subset of the edges
    random.shuffle(edges)
    sub = edges[:numEdges_sample]
    
    # Create a copy of the graph
    Gcp = G.copy()
    
    # Add the edges to the copied graph
    Gcp.add_edges_from(sub)
    
    
    
    ### Compute the B value
    # - B_ij = (A - (k_i-k_j)/2m)
    #    - A_ij = Number of edges between node i and j
    #    - k_i = degree of node i
    #    - k_j = degree of node j
    #    - m = number of edges in the old graph
    
    # The B matrix
    B_ij = []
    
    # Calculate the m value
    m = numEdges_sample
    
    # Iterate over all nodes in the old graph (i)
    for i in list(Gcp.nodes):
        neighbors_i = list(Gcp.neighbors(i))
        k_i = len(neighbors_i)
        
        # B vector for node i
        B_i = []
        
        # Iterate over all nodes in the new graph (j)
        for j in list(Gcp.nodes):
            # Calculate the B value
            neighbors_j = list(Gcp.neighbors(j))
            k_j = len(neighbors_j)
            #A_ij = 1 if ((i, j) in G.edges or (j, i) in G.edges) else 0
            A_ij = len(list(set(neighbors_i) & set(neighbors_j)))
            
            B = A_ij - (k_i*k_j)/(2*m)
        
            # Add the value to the B vector
            B_i.append(B)
        
        # Add the vector to the B matrix
        B_ij.append(B_i)
    
    # Save the B matrix to the file
    np.save(file, B_ij, allow_pickle=False)