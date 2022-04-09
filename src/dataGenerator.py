from networkx import graphml
import networkx as nx
from names import get_full_name
import random

# Note: Change These Parameters to Configure as Discussed in the Readme

# Hyper Parameters
outFile = "../data/dataset.graphml"  # File to Save Graph to
vertices = 128  # Number of vertices In Graph (Nodes)
communities = 4  # Number of Communities in Graph
communitySize = vertices//communities   # Number of Vertices in Each Community
rand = True  # True to Generate Random Values
names = True  # True to Generate Random Names
P_out = 0.03  # Probability of Edge Between Vertices of Different Group
P_in = -4.1171 * P_out + 0.3063  # Probability of Edge Between Vertices of Same Group
stats = True  # True to see Stats After Running

# Necessary Assertion
assert P_in > P_out

# Initialize Graph
G = nx.Graph()

# Classify Each Node into a Community
comm = sum([[i for j in range(0, communitySize)] for i in range(0, communities)], [])
while len(comm) < vertices:
    comm.append(random.choice([i for i in range(0, communitySize)]))
random.shuffle(comm)

# Add Nodes to Graph

# Store Name
if names:
    nodes = []
    vals = []
    
    # Store Vertices Number of Nodes
    for i in range(0, vertices - 1):

        # Get a Name
        v = get_full_name()
        
        # Ensure the Name is New
        while v in vals:
            v = get_full_name()
        
        # Store Name
        nodes.append((v, {"community": comm[i]}))
        vals.append(v)
    
    vals.append("Sussy Baka")  # Hehe Rawr (●´ω｀●)
    nodes.append(("Sussy Baka", {"community": comm[i]}))
        
# Store Sequential Numbers
elif not rand:
    vals = [i for i in range(0, vertices)]
    nodes = [(i, {"community": comm[i]}) for i in range(0, vertices)]
    
# Store Random Numbers
elif rand:
    nodes = []
    vals = []
    
    # Store Vertices Number of Nodes
    for i in range(0, vertices):

        # Get a Random Number
        v = random.randint(0, vertices * 100)
        
        # Ensure the Number is New
        while v in vals:
            v = random.randint(0, vertices * 100)
        
        # Store Number
        nodes.append((v, {"community": comm[i]}))
        vals.append(v)

# Add Nodes to Graph
G.add_nodes_from(nodes)

# Add Edges

# Iterate over all Nodes
for n1 in range(0, vertices):

    # Iterate over all Nodes Again Without Connections to Current (n1)
    for n2 in range(0, vertices):

        # If Nodes are Equal, Skip Iteration
        if vals[n1] == vals[n2]:
            continue
        
        # Get a Random Value Between 0 and 1.
        v = random.random()
        
        # If the Nodes are Part of the Same Community and the Random
        # Value is Less than P_in, add an Edge Between the Two Nodes
        if comm[n1] == comm[n2] and v < P_in:
            G.add_edge(vals[n1], vals[n2])
        
        # If the Nodes are not Part of the Same Community and the Random
        # Value is Less than P_out, add an Edge Between the Two Nodes
        elif comm[n1] != comm[n2] and v < P_out:
            G.add_edge(vals[n1], vals[n2])

# Save Graph
graphml.write_graphml(G, outFile)

# If Stats, Show Stats on the Graph
if stats:

    # Get the Average Degree of all Nodes
    
    # Holds all Nodes Degree Counts
    # Format: node: {Total, in count, out count}
    degreeCts = dict()
    
    # Iterate over all Edges in the Graph
    for e in list(G.edges):

        # Increase the Degree Counts for Each Part of the Edge
        
        # Make sure the Edges are in the Dictionary
        if e[0] not in degreeCts.keys():
            degreeCts[e[0]] = [0, 0, 0]
        if e[1] not in degreeCts.keys():
            degreeCts[e[1]] = [0, 0, 0]
        
        # If the Communities are the Same, Increase in Count for Both Edges
        if comm[vals.index(e[0])] == comm[vals.index(e[1])]:
            degreeCts[e[0]][1] += 1
            degreeCts[e[1]][1] += 1

        # If the Communities are Different, Increase the out Count for Both Edges
        else:
            degreeCts[e[0]][2] += 1
            degreeCts[e[1]][2] += 1
        
        # Increase Total Count of Both Edges
        degreeCts[e[0]][0] += 1
        degreeCts[e[1]][0] += 1
    
    # Get Average of the Degree Counts
    print(f"Number of nodes: {len(degreeCts.keys())}")
    print(f"Number of edges: {len(list(G.edges))}")
    print(f"Average degree count: {sum([i[0] for i in degreeCts.values()])/len(degreeCts.keys())}")
    print(f"Average in degree count: {sum([i[1] for i in degreeCts.values()])/len(degreeCts.keys())}")
    print(f"Average out degree count: {sum([i[2] for i in degreeCts.values()])/len(degreeCts.keys())}")
