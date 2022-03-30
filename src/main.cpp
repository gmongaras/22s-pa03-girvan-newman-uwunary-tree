#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/breadth_first_search.hpp>

#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>
<<<<<<< Updated upstream
#include <boost/property_map/property_map.hpp>
=======

>>>>>>> Stashed changes
#include <fstream>
#include <string>
#include <iostream>
#include <istream>

struct GraphData { std::string Name; };
struct VertexProperty { std::string Name; };
struct EdgeProperty { std::string Name; };

using Graph = boost::adjacency_list<boost::setS, boost::vecS, boost::directedS, VertexProperty, EdgeProperty, GraphData>;

<<<<<<< Updated upstream
Graph ReadGraph(std::istream& is) {
=======
    //std::istringstream graphml("data/football/football.graphml");
    std::filebuf fb;
    fb.open("data/football/football.graphml", std::ios::in);
    std::istream graphml(&fb);
    typedef boost::adjacency_list<> Graph;
>>>>>>> Stashed changes
    Graph graph;
    boost::dynamic_properties dp(boost::ignore_other_properties);
    dp.property("Name", boost::get(&VertexProperty::Name, graph));

    boost::read_graphml(is, graph, dp);

    return graph;
}

extern std::string const graphml_111;

int main() {
    std::istringstream is(graphml_111);
    Graph g = ReadGraph(is);
    print_graph(g, get(&VertexProperty::Name, g));
}

std::string const graphml_111 = R"(<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <key id="key0" for="node" attr.name="Name" attr.type="string" />
  <graph id="G" edgedefault="directed" parse.nodeids="canonical" parse.edgeids="canonical" parse.order="nodesfirst">
    <node id="n0">
      <data key="key0">A</data>
    </node>
    <node id="n1">
      <data key="key0">D</data>
    </node>
    <node id="n2">
      <data key="key0">B</data>
    </node>
    <node id="n3">
      <data key="key0">C</data>
    </node>
    <edge id="e0" source="n0" target="n1">
    </edge>
    <edge id="e1" source="n2" target="n3">
    </edge>
  </graph>
</graphml>)";