// Some Useful Links:
// https://stackoverflow.com/questions/58974799/how-can-i-solve-this-error-in-printing-nodes-and-edges-boost-graph-library
// https://stackoverflow.com/questions/49047897/boost-read-graphml-doesnt-read-xml-properly-it-gives-all-the-vertices-but-they

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>
#include <boost/property_map/property_map.hpp>

#include <fstream>

struct VertexProperty { long value; }; // Vertex ID
struct EdgeProperty { double weight = 0; }; // Weight Value (Set 0)

using boost::make_iterator_range; // Iteration
using Graph = boost::adjacency_list<boost::setS, boost::vecS, boost::undirectedS, VertexProperty, EdgeProperty>; // Graph

Graph ReadGraph(std::ifstream& I) {
    Graph G; // Creates Return Variable
    boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties
    D.property("Value", boost::get(&VertexProperty::value, G)); // Vertex
    boost::read_graphml(I, G, D); // Read In Program Argument Graphml
    return G; // Return Temp Graph
}

// Prints Important Information
void PrintGraph(Graph const &G) {
    std::cout << "Initial Statistics:\n";
    std::cout << "Number of Vertices is :\t" << num_vertices(G) << "\n";
    std::cout << "Number of Edges is :\t" << num_edges(G) << "\n\n";

    // Prints All Connections From All Nodes (Using ID)
    boost::print_graph(G, boost::get(&VertexProperty::value, G), std::cout);

    // Prints All Node Weights, Edges (Can Change)
    std::cout << "\n";
    for (auto v : make_iterator_range(vertices(G))) {
        for (auto oe : make_iterator_range(out_edges(v, G))) {
            std::cout << "Edge " << oe << " Weight " << G[oe].weight << "\n";
        }
    }
}

// Handles Main Graph ( PrintGraph(G); )
int main(int argc, char* argv[]) {
    if (argc >= 2) {
        std::ifstream I(argv[1]);
        Graph G = ReadGraph(I); }
    else {
        // Call Python Script
    }
}