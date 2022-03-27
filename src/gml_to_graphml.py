from networkx import gml
from networkx import graphml


# Filename to convert
inFile = "../data/football/football.gml"

# Filename to write to
outFile = inFile[:inFile.rfind(".")] + ".graphml"


# Load in the graph
G = gml.read_gml(inFile)

# Convert the graph and save it
graphml.write_graphml(G, outFile)
