from networkx import gml
from networkx import graphml

# Filename to Convert
inFile = "../data/football/football.gml"

# Filename to Write to
outFile = inFile[:inFile.rfind(".")] + ".graphml"

# Load in Graph
G = gml.read_gml(inFile)

# Convert and Save Graph
graphml.write_graphml(G, outFile)
