#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>
#include <boost/property_map/property_map.hpp>

#include <fstream>

//struct GraphData { std::string Name; };
//struct VertexProperty { std::string Name; };
//struct EdgeProperty { std::string Name; };
//
//Graph ReadGraph(std::istream& in) {
//
//    Graph graph; // Creates Graph Named G
//    boost::dynamic_properties dp; //(boost::ignore_other_properties); // Ignore Any Unmapped Extraneous Properties
////    DP.property("Name", boost::get(&VertexProperty::Name, G));
//    boost::read_graphml(in, graph, dp);
//    return graph;
//}

int main() {

    std::istringstream graphml("data/football/football.graphml");
    typedef boost::adjacency_list<> Graph;
    Graph graph;
    boost::dynamic_properties dp;

    boost::read_graphml(graphml, graph, dp);

//    print_graph(graph, get(&VertexProperty::Name, graph));
}