// Some Useful Links:
// https://stackoverflow.com/questions/58974799/how-can-i-solve-this-error-in-printing-nodes-and-edges-boost-graph-library
// https://stackoverflow.com/questions/49047897/boost-read-graphml-doesnt-read-xml-properly-it-gives-all-the-vertices-but-they
// https://www.codeproject.com/Articles/820116/Embedding-Python-program-in-a-C-Cplusplus-code (Python Embedding)
// https://stackoverflow.com/questions/16962430/calling-python-script-from-c-and-using-its-output (Python Embedding)

// Boost Includes
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/subgraph.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>

// Standard Includes
#include <Python.h>
#include <fstream>
#include <random>
#include <string>
#include <map>
#include <list>

// Adjacency List, Basic Node, Standard Edge Definitions
typedef boost::adjacency_list<boost::setS, boost::vecS, boost::undirectedS> Graph;
typedef boost::property_map<Graph, boost::vertex_index_t>::type IndexMap;
typedef std::map<std::tuple<float, float>, float> EdgeStd;

// Nowode Class! OwO :)
class Node {

public:
    int level; // Level of Node
    float value; // Value Stored Within Node
    float shortestPaths = 1; // Number of Shortest Paths that can Reach this Node from Root
    std::vector<Node> children; // Children of Node
    std::vector<Node> parents; // Parents of Node
    std::vector<Node> sameLevel; // Nodes on Same Level
    bool labelled = false; // Has Node Been Visited in BFS?

    // Constructor, Must be Called
    Node(float value, int level) {
        this->value = value;
        this->level = level;
    }

    // Add Child to Node
    void addChild(Node& c) {
        children.push_back(c);
        c.parents.push_back(*this);
    }

    // Add Parent to Node
    void addParent(Node& p) {
        parents.push_back(p);
        p.children.push_back(*this);
        shortestPaths += 1;
    }

    // Tests if two Nodes are Equal
    bool operator==(Node& n) const {
        return value == n.value;
    }

};

// Prints Important Information
void PrintGraph(Graph const& G) {
    std::cout << "Vertex Amount: " << num_vertices(G) << "\n";
    std::cout << "Edge Amount: " << num_edges(G) << "\n";
    auto es = boost::edges(G);
    for (auto eit = es.first; eit != es.second; ++eit) {
        std::cout << boost::source(*eit, G) << ' ' << boost::target(*eit, G) << std::endl;
    }
}

// Reads In Graph
Graph ReadGraph(std::ifstream& I) {
    Graph G; // Creates Return Variable
    boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties
    boost::read_graphml(I, G, D); // Read In Program Argument Graphml
    return G; // Return Variable
}

// Inputs:
// node = Node of Tree of Graph
// parent = Parent of Given Node
// edges = Dictionary of Edges
// Outputs:
// None (Edges Changed Within Function)
void edgeLabelling(Node& node, Node& parent, EdgeStd& edges) {

    // Used Throughout, Starts at
    // 1 For Less Hassle Later
    float betweenness = 1;

    if (node.labelled) {

        // Divide Betweenness of Parent Nodes
        // If Root Node, Iterate to the Child Nodes and Calculate Their Betweenness
        // If Leaf Node, Calculate Betweenness of the Edges Between it and Parent
        if (node.children.empty()) { betweenness /= float(node.parents.size()); }
        else { betweenness = node.shortestPaths / float(node.parents.size()); }

        // Store Betweenness of Node and Parent
        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent.value, node.value)) != edges.end()) {
            edges[std::make_tuple(parent.value, node.value)] += betweenness; }
        else if (edges.find(std::make_tuple(node.value, parent.value)) != edges.end()) {
            edges[std::make_tuple(node.value, parent.value)] += betweenness; }
        else { edges[std::make_tuple(parent.value, node.value)] = betweenness; }

        return;

    }

    // If Node is a Leaf Node, Not Labelled
    if (node.children.empty()) {

        betweenness /= float(node.parents.size());

        // Store Betweenness of Node and Parent
        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent.value, node.value)) != edges.end()) {
            edges[std::make_tuple(parent.value, node.value)] += betweenness; }
        else if (edges.find(std::make_tuple(node.value, parent.value)) != edges.end()) {
            edges[std::make_tuple(node.value, parent.value)] += betweenness; }
        else { edges[std::make_tuple(parent.value, node.value)] = betweenness; }

    }

    // If Node isn't a Leaf Node
    else {

        // Calculate Betweenness of all Children
        for (auto cNode : node.children) {
            edgeLabelling(cNode, node, edges); }

        for (auto cNode : node.children) {

            try { // If No Key Exists, Stop Program

                // Does Key (node, child) Exist?
                // Does Key (child, node) Exist?
                // Throw Exception, Stop Program
                if (edges.find(std::make_tuple(node.value, cNode.value)) != edges.end()) {
                    betweenness += edges[std::make_tuple(node.value, cNode.value)]; }
                else if (edges.find(std::make_tuple(cNode.value, node.value)) != edges.end()) {
                    betweenness += edges[std::make_tuple(cNode.value, node.value)]; }
                else { throw std::invalid_argument("Key Must Exist"); }

            } catch (std::invalid_argument& e) { std::cerr << e.what() << std::endl; }

        }

        // Update shortestPaths Value of Node
        node.shortestPaths = betweenness;

        // Divide Betweenness Between Parent Nodes
        betweenness /= float(node.parents.size());

        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent.value, node.value)) != edges.end()) {
            edges[std::make_tuple(parent.value, node.value)] += betweenness; }
        else if (edges.find(std::make_tuple(node.value, parent.value)) != edges.end()) {
            edges[std::make_tuple(node.value, parent.value)] += betweenness; }
        else { edges[std::make_tuple(parent.value, node.value)] = betweenness; }

    }

    // Label Node Visited
    node.labelled = true;

}

// Inputs:
// G = Our Graph
// n = Index of Node to find Paths
// edges = Dictionary of Edges
// Outputs:
// None (Edges Changed Within Function)
void SSSP(Graph const& G, unsigned long n, EdgeStd& edges) {

    // Visited nodes, Tree Initialization
    std::vector<Node> visited;
    auto tree = Node(n, 1);

    // Step 1, 2 = BFS, Node Labelling

    // Stack Used for BFS, Push Root Node
    std::stack<Node> s;
    s.push(tree);
    visited.push_back(tree);

    // Current Level of Tree
    int level = 1;

    // Iterate Until Empty Stack
    while (!s.empty()) {

        // Get Top, Pop Stack
        auto curr = s.top();
        s.pop();

        // Current Level = Level + 1
        level = curr.level + 1;

        // Iterate over all Adjacent Nodes
        auto neighbors = boost::adjacent_vertices((curr.value), G);
        for (auto nNode : make_iterator_range(neighbors)) {
            auto node = Node(nNode, level);

            int loc; // Iterator
            bool isFound = false;

            // Try (No ValueError): Get Index of Node in Visited List
            for (loc = 0; loc < visited.size(); loc++) {
                if (visited[loc] == node) {
                    isFound = true;
                    break;
                }
            }

            // Catch (No ValueError): If Node is Unvisited, Push
            if (!isFound) {
                s.push(node);
                visited.push_back(node);
                curr.addChild(node);
                continue;
            }

            // Reusing isFound, Set Node
            isFound = false;
            node = visited[loc];

            // If Node is Equal to Curr Level, Set Equal Level
            if (node.level == curr.level) {
                for (auto sNode : node.sameLevel) {
                    if (curr == sNode) { isFound = true; } }
                if (!isFound) {
                    node.sameLevel.push_back(curr);
                    curr.sameLevel.push_back(node); }
            }

            // If Node has Smaller Level than Current Node,
            // Set this Node as the Parent of the Current Node
            else if (node.level < curr.level) {
                for (auto pNode : curr.parents) {
                    if (node == pNode) { isFound = true; } }
                if (!isFound) { curr.addParent(node); }
            }
        }
    }

    // Step 3 = Edge Labelling

    // Iterate Over All Root Node Children
    EdgeStd bet;
    for (auto cNode : tree.children) {
        edgeLabelling(cNode, tree, bet);
    }

    // Add Betweenness to Total Edges Dictionary
    for (auto kvPair : bet) {
        auto edge = kvPair.first;

        // Does the Edge Exist?
        // Does the Reverse Exist?
        // Add Edge if not Existing
        if (edges.find(edge) != edges.end()) {
            edges[edge] += bet[edge] / 2; }
        else if (edges.find(std::make_tuple(std::get<1>(edge), std::get<0>(edge))) != edges.end()) {
            edges[std::make_tuple(std::get<1>(edge), std::get<0>(edge))] += bet[edge] / 2; }
        else { edges[edge] = bet[edge] / 2; }

    }
}

// Inputs:
// G = Our Graph
// Output
// Edges - The Betweenness of all Edges
EdgeStd calculateBetweenness(Graph const& G) {

    // The Betweenness of Graph
    EdgeStd betweenness;

    // Get Property Map for Vertices, Iterate, Pass Index to Function
    // Calculate Betweenness for all Paths from that Node
    IndexMap index = get(boost::vertex_index, G);
    for (auto n = vertices(G); n.first != n.second; ++n.first) {
        SSSP(G, index[*n.first], betweenness); }

    return betweenness;

}

// Use the Normal Q value to
// Stop Loop when Removing

// Inputs:
// G = Our Graph
// Outputs:
// G = New Graph (Removed Edges
Graph normalLoop(Graph const &G) {

    // Iterate Until Q Value isn't Increasing
    int Q_prev = INT_MIN;
    int Q = INT_MIN;
    int* maxBetweenness = new int[0];
    int i = 1;

    while (Q + 0.05 >= Q_prev) { // Update Q_prev Value

        Q_prev = Q;

        // Calculate Betweenness of All Edges in Graph
        auto betweenness = calculateBetweenness(G);

        // If Betweenness Empty, Break Loop
        if (betweenness.empty()) break;

        // FIXME

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