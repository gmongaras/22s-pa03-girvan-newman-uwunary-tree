// Some Useful Links:
// https://stackoverflow.com/questions/58974799/how-can-i-solve-this-error-in-printing-nodes-and-edges-boost-graph-library
// https://stackoverflow.com/questions/49047897/boost-read-graphml-doesnt-read-xml-properly-it-gives-all-the-vertices-but-they
// https://www.codeproject.com/Articles/820116/Embedding-Python-program-in-a-C-Cplusplus-code (Python Embedding)
// https://stackoverflow.com/questions/16962430/calling-python-script-from-c-and-using-its-output (Python Embedding)

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>
#include <boost/property_map/property_map.hpp>

#include <fstream>
#include <Python.h>
#include <string>

struct VertexProperty { long value; }; // Vertex ID (Community Number)
using Graph = boost::adjacency_list<boost::setS, boost::vecS, boost::undirectedS, VertexProperty>;
using vertex_descriptor = boost::graph_traits<Graph>::vertex_descriptor;

Graph ReadGraph(std::ifstream& I) {
    Graph G; // Creates Return Variable
    boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties

    //boost::dynamic_properties dp;
    //D.property("Name", boost::get(&GraphData::Name, G));

    D.property("value", boost::get(&VertexProperty::value, G)); // Vertex ID Getter
    D.property("id", boost::get(&VertexProperty::id, G)); // Vertex ID Getter
    boost::read_graphml(I, G, D); // Read In Program Argument Graphml
    return G; // Return Variable
}

// Prints Important Information
void PrintGraph(Graph const &G) {
    std::cout << "Vertex Amount: " << num_vertices(G) << "\n";
    std::cout << "Edge Amount: " << num_edges(G) << "\n";

    // Prints All Connections From All Nodes (Using ID)
    boost::print_graph(G, boost::get(&VertexProperty::value, G), std::cout);

    // Prints All Edges
    auto es = boost::edges(G);
    for (auto eit = es.first; eit != es.second; ++eit) {
        std::cout << boost::source(*eit, G) << ' ' << boost::target(*eit, G) << std::endl;
    }
}


// Handles Main Graph ( PrintGraph(G); )
// Argument Example: data/football/football.graphml
int main(int argc, char* argv[]) {
    if (argc >= 2) {
        std::ifstream I(argv[1]);
        Graph G = ReadGraph(I);

        boost::queue<vertex_descriptor> Q;
        boost::default_bfs_visitor V;

        auto index_map = boost::get(boost::vertex_index, G);
        auto color_map = boost::make_vector_property_map<boost::default_color_type>(index_map);

//        for (auto vd : boost::make_iterator_range(vertices(G))) {
//            std::cout << "vertex descriptor #" << vd
//                      << " degree:" << degree(vd, G)
//                      << " community:"     << G[vd].value
//                      << "\n";
//        }

        for (auto vd : boost::make_iterator_range(vertices(G))) {
            boost::breadth_first_search(G, vd, Q, V, color_map); // Time Complexity: O(E + V)
        }
    }
    else {
        Py_Initialize(); // Initialize Environment
//        PyRun_SimpleString("import sys"); // Call Import
//        PyRun_SimpleString("sys.path.append('/src/dataGenerator.py')"); // Can't Get it to work!
        Py_Finalize(); // End Environment
    }
}