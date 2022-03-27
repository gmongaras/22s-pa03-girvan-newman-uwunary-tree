from tkinter import E
from networkx import graphml
import networkx as nx
from names import get_full_name
import random



# Hyperparameters
outFile = "dataset.graphml"             # File to save the graph to
vertices = 128                          # Number of vertices (nodes) in the graph
communities = 4                         # Number of communities in the graph
communitySize = vertices//communities   # Number of vertices in each community
rand = True                             # True to generate random values
names = True                            # True to generate random names
P_out = 0.03                            # Probability of edge between vertices of different group
P_in = 23/vertices                      # Probability of edge between vertices of same group
stats = True                            # True to see stats after running


# Make sure P_in is greater than P_out
assert P_in > P_out



# Initialize the graph
G = nx.Graph()



# Add the nodes to the graph
if names == True:
    nodes = [get_full_name() for i in range(0, vertices)]
elif rand == False:
    nodes = [i for i in range(0, vertices)]
elif rand == True:
    nodes = [random.randint(0, vertices*100) for i in range(0, vertices)]
G.add_nodes_from(nodes)
while len(list(G.nodes)) < vertices:
    if names == True:
        G.add_node(get_full_name())
    elif rand == True:
        G.add_node(random.randint(0, vertices*100))

# Classify each node into a community
comm = sum([[i for j in range(0, communitySize)] for i in range(0, communities)], [])
random.shuffle(comm)



### Add the edges

# Iterate over all nodes
for n1 in range(0, vertices):
    # Iterate over all nodes again without connections
    # to the current node, n1
    for n2 in range(0, vertices):
        # If the nodes are equal, skip this iteration
        if nodes[n1] == nodes[n2]:
            continue
        
        # Get a random value between 0 and 1.
        v = random.random()
        
        # If the nodes are a part of the same community and the
        # random value is less than P_in, add an edge between
        # the two nodes
        if comm[n1] == comm[n2] and v < P_in:
            G.add_edge(nodes[n1], nodes[n2])
        
        # If the nodes are not a part of the same community and the
        # ranodm value is less than P_out, add an edge between
        # the two nodes
        elif comm[n1] != comm[n2] and v < P_out:
            G.add_edge(nodes[n1], nodes[n2])


# Save the graph
graphml.write_graphml(G, outFile)


# If stats is True, show stats on the graph
if stats == True:
    ### Get the average degree of all nodes
    
    # Holds all nodes degree counts
    # Format:
    #   node: {Total, in count, out count}
    degreeCts = dict()
    
    # Iterate over all edges in the graph
    for e in list(G.edges):
        ## Increase the degree counts for each part of the edge
        
        # Make sure the edges are in the dictionary
        if e[0] not in degreeCts.keys():
            degreeCts[e[0]] = [0, 0, 0]
        if e[1] not in degreeCts.keys():
            degreeCts[e[1]] = [0, 0, 0]
        
        # If the communities are the same, increase the in count
        # for both edges
        if comm[nodes.index(e[0])] == comm[nodes.index(e[1])]:
            degreeCts[e[0]][1] += 1
            degreeCts[e[1]][1] += 1
        # If the communities are different, increase the out count
        # for both edges
        else:
            degreeCts[e[0]][2] += 1
            degreeCts[e[1]][2] += 1
        
        # Increase the total count of both edges
        degreeCts[e[0]][0] += 1
        degreeCts[e[1]][0] += 1
    
    # Get the average of the degree counts
    print(f"Number of nodes: {len(degreeCts.keys())}")
    print(f"Number of edges: {len(list(G.edges))}")
    print(f"Average degree count: {sum([i[0] for i in degreeCts.values()])/len(degreeCts.keys())}")
    print(f"Average in degree count: {sum([i[1] for i in degreeCts.values()])/len(degreeCts.keys())}")
    print(f"Average out degree count: {sum([i[2] for i in degreeCts.values()])/len(degreeCts.keys())}")