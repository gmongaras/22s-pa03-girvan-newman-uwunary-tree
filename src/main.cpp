// Some Useful Links:
// https://stackoverflow.com/questions/58974799/how-can-i-solve-this-error-in-printing-nodes-and-edges-boost-graph-library
// https://stackoverflow.com/questions/49047897/boost-read-graphml-doesnt-read-xml-properly-it-gives-all-the-vertices-but-they
// https://www.codeproject.com/Articles/820116/Embedding-Python-program-in-a-C-Cplusplus-code (Python Embedding)
// https://stackoverflow.com/questions/16962430/calling-python-script-from-c-and-using-its-output (Python Embedding)

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/subgraph.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>

#include <fstream>
#include <Python.h>
#include <random>
#include <string>
#include <map>
#include <list>

// Adjacency List
typedef boost::adjacency_list<boost::setS, boost::vecS, boost::undirectedS> Graph;

class Node {

};

// Prints Important Information
void PrintGraph(Graph const &G) {
    std::cout << "Vertex Amount: " << num_vertices(G) << "\n";
    std::cout << "Edge Amount: " << num_edges(G) << "\n";
    auto es = boost::edges(G);
    for (auto eit = es.first; eit != es.second; ++eit) {
        std::cout << boost::source(*eit, G) << ' ' << boost::target(*eit, G) << std::endl;
    }
}

Graph ReadGraph(std::ifstream& I) {
    Graph G; // Creates Return Variable
    boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties
    boost::read_graphml(I, G, D); // Read In Program Argument Graphml
    return G; // Return Variable
}

// Shuffle List Contents
template < typename T > void shuffle( std::list<T>& lst )
{
    // create a vector of (wrapped) references to elements in the list
    // http://en.cppreference.com/w/cpp/utility/functional/reference_wrapper
    std::vector< std::reference_wrapper< const T > > vec( lst.begin(), lst.end() ) ;

    // shuffle (the references in) the vector
    std::shuffle( vec.begin(), vec.end(), std::mt19937{ std::random_device{}() } ) ;

    // copy the shuffled sequence into a new list
    std::list<T> shuffled_list {  vec.begin(), vec.end() } ;

    // swap the old list with the shuffled list
    lst.swap(shuffled_list) ;
}

void SSSP(Graph const &G,
          boost::list_edge<unsigned long, boost::no_property>& n,
          std::map<std::tuple<int, int>, float> edges) {

}

std::map<std::tuple<int, int>, float> calculateBetweenness(Graph const &G) {

     std::map<std::tuple<int, int>, float> betweenness;
     auto edges = G.m_edges;
     shuffle(edges);

     for (auto& n : edges) {
         SSSP(G, n, betweenness);
     }

     return betweenness;

}

Graph normalLoop(Graph const &G) {

    int Q_prev = INT_MIN;
    int Q = INT_MIN;
    int* maxBetweenness = new int[0];
    int i = 1;

    while (Q + 0.05 >= Q_prev) {
        Q_prev = Q;
        auto betweenness = calculateBetweenness(G);
    }

}

// Handles Main Graph ( PrintGraph(G); )
// Argument Example: data/football/football.graphml
int main(int argc, char* argv[]) {
    if (argc >= 2) {
        std::ifstream I(argv[1]);
        Graph G = ReadGraph(I);

        G = normalLoop(G);

//        boost::queue<vertex_descriptor> Q;
//        boost::default_bfs_visitor V;
//
//        auto index_map = boost::get(boost::vertex_index, G);
//        auto color_map = boost::make_vector_property_map<boost::default_color_type>(index_map);
//
////        for (auto vd : boost::make_iterator_range(vertices(G))) {
////            std::cout << "vertex descriptor #" << vd
////                      << " degree:" << degree(vd, G)
////                      << " community:"     << G[vd].value
////                      << "\n";
////        }
//
//        for (auto vd : boost::make_iterator_range(vertices(G))) {
//            boost::breadth_first_search(G, vd, Q, V, color_map); // Time Complexity: O(E + V)
//        }
    }
    else {
        Py_Initialize(); // Initialize Environment
//        PyRun_SimpleString("import sys"); // Call Import
//        PyRun_SimpleString("sys.path.append('/src/dataGenerator.py')"); // Can't Get it to work!
        Py_Finalize(); // End Environment
    }
}