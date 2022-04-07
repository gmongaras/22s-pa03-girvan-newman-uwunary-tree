// Boost Includes
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/property_map/dynamic_property_map.hpp>
#include <boost/graph/copy.hpp>

// Standard Includes
#include <fstream>
#include <random>
#include <string>
#include <map>

// Adjacency List, Basic Node, Standard Edge Definitions
struct VertexProperty { long value; }; // Vertex ID
typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, VertexProperty> Graph;
typedef boost::property_map<Graph, boost::vertex_index_t>::type IndexMap;
typedef std::map<std::tuple<unsigned long, unsigned long>, float> EdgeStd;

// Nowode Class! OwO :)
class Node {

public:
    int level; // Level of Node
    unsigned long value; // Value Stored Within Node
    float shortestPaths = 1; // Number of Shortest Paths that can Reach this Node from Root
    std::vector<Node*> children; // Children of Node
    std::vector<Node*> parents; // Parents of Node
    std::vector<Node*> sameLevel; // Nodes on Same Level
    bool labelled = false; // Has Node Been Visited in BFS?

    // Constructor, Must be Called
    Node(unsigned long value, int level) {
        this->value = value;
        this->level = level;
    }

    // Add Child to Node
    void addChild(Node* c) {
        children.push_back(c);
        c->parents.push_back(this);
    }

    // Add Parent to Node
    void addParent(Node* p) {
        parents.push_back(p);
        p->children.push_back(this);
        shortestPaths += 1;
    }

    // Tests if two Nodes are Equal
    bool operator==(Node n) const {
        return value == n.value;
    }

};

// Prints Important Information
void PrintGraph(Graph& G) {
    std::cout << "Vertex Amount: " << num_vertices(G) << "\n";
    std::cout << "Edge Amount: " << num_edges(G) << "\n";
    boost::print_graph(G, boost::get(&VertexProperty::value, G), std::cout);
    auto es = boost::edges(G);
    for (auto eit = es.first; eit != es.second; ++eit) {
        std::cout << boost::source(*eit, G) << ' ' << boost::target(*eit, G) << std::endl;
    }
}

// Reads In Graph
Graph ReadGraph(std::ifstream& I, char* attName) {
    Graph G; // Creates Return Variable
    boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties
    D.property(attName, boost::get(&VertexProperty::value, G)); // Vertex ID Getter
    boost::read_graphml(I, G, D); // Read In Program Argument Graphml
    return G; // Return Variable
}

// Inputs:
// node = Node of Tree of Graph
// parent = Parent of Given Node
// edges = Dictionary of Edges
// Outputs:
// None (Edges Changed Within Function)
void edgeLabelling(Node*& node, Node*& parent, EdgeStd& edges) {

    // Used Throughout, Starts at
    // 1 For Less Hassle Later
    float betweenness = 1;

    if (node->labelled) {

        // Divide Betweenness of Parent Nodes
        // If Root Node, Iterate to the Child Nodes and Calculate Their Betweenness
        // If Leaf Node, Calculate Betweenness of the Edges Between it and Parent
        if (node->children.empty()) { betweenness /= float(node->parents.size()); }
        else { betweenness = node->shortestPaths / float(node->parents.size()); }

        // Store Betweenness of Node and Parent
        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent->value, node->value)) != edges.end()) {
            edges[std::make_tuple(parent->value, node->value)] += betweenness; }
        else if (edges.find(std::make_tuple(node->value, parent->value)) != edges.end()) {
            edges[std::make_tuple(node->value, parent->value)] += betweenness; }
        else { edges[std::make_tuple(parent->value, node->value)] = betweenness; }

        return;

    }

    // If Node is a Leaf Node, Not Labelled
    if (node->children.empty()) {

        betweenness /= float(node->parents.size());

        // Store Betweenness of Node and Parent
        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent->value, node->value)) != edges.end()) {
            edges[std::make_tuple(parent->value, node->value)] += betweenness; }
        else if (edges.find(std::make_tuple(node->value, parent->value)) != edges.end()) {
            edges[std::make_tuple(node->value, parent->value)] += betweenness; }
        else { edges[std::make_tuple(parent->value, node->value)] = betweenness; }

    }

    // If Node isn't a Leaf Node
    else {

        // Calculate Betweenness of all Children
        for (Node* cNode : node->children) {
            edgeLabelling(cNode, node, edges); }

        for (auto cNode : node->children) {

            try { // If No Key Exists, Stop Program

                // Does Key (node, child) Exist?
                // Does Key (child, node) Exist?
                // Throw Exception, Stop Program
                if (edges.find(std::make_tuple(node->value, cNode->value)) != edges.end()) {
                    betweenness += edges[std::make_tuple(node->value, cNode->value)]; }
                else if (edges.find(std::make_tuple(cNode->value, node->value)) != edges.end()) {
                    betweenness += edges[std::make_tuple(cNode->value, node->value)]; }
                else { throw std::invalid_argument("Key Must Exist"); }

            } catch (std::invalid_argument& e) { std::cerr << e.what() << std::endl; }

        }

        // Update shortestPaths Value of Node
        node->shortestPaths = betweenness;

        // Divide Betweenness Between Parent Nodes
        betweenness /= float(node->parents.size());

        // Does Key (parent, child) Exist?
        // Does Key (child, parent) Exist?
        // Add Key (parent, child)
        if (edges.find(std::make_tuple(parent->value, node->value)) != edges.end()) {
            edges[std::make_tuple(parent->value, node->value)] += betweenness; }
        else if (edges.find(std::make_tuple(node->value, parent->value)) != edges.end()) {
            edges[std::make_tuple(node->value, parent->value)] += betweenness; }
        else { edges[std::make_tuple(parent->value, node->value)] = betweenness; }

    }

    // Label Node Visited
    node->labelled = true;

}

// Inputs:
// G = Our Graph
// n = Index of Node to find Paths
// edges = Dictionary of Edges
// Outputs:
// None (Edges Changed Within Function)
void SSSP(Graph& G, unsigned long n, EdgeStd& edges) {

    // Visited nodes, Tree Initialization
    std::vector<Node*> visited;
    std::vector<Node*> deleteHelper;
    std::vector<Node*> deleteHelperSmall;
    Node* tree = new Node(n, 1);

    // Step 1, 2 = BFS, Node Labelling

    // Stack Used for BFS, Push Root Node
    std::stack<Node*> s;
    s.push(tree);
    visited.push_back(tree);
    deleteHelperSmall.push_back(tree);

    // Current Level of Tree
    int level;

    // Iterate Until Empty Stack
    while (!s.empty()) {

        // Get Top, Pop Stack
        Node* curr = s.top();
        s.pop();

        // Current Level = Level + 1
        level = curr->level + 1;

        // Iterate over all Adjacent Nodes
        auto neighbors = boost::adjacent_vertices((curr->value), G);
        for (auto nNode : make_iterator_range(neighbors)) {
            Node* node = new Node(nNode, level);
            deleteHelper.push_back(node);

            int loc; // Iterator
            bool isFound = false;

            // Try (No ValueError): Get Index of Node in Visited List
            for (loc = 0; loc < visited.size(); loc++) {
                if (*visited[loc] == *node) {
                    isFound = true;
                    break;
                }
            }

            // Catch (No ValueError): If Node is Unvisited, Push
            if (!isFound) {
                s.push(node);
                visited.push_back(node);
                curr->addChild(node);
                continue;
            }

            // Reusing isFound, Set Node
            isFound = false;
            node = visited[loc];

            // If Node is Equal to Curr Level, Set Equal Level
            if (node->level == curr->level) {
                for (auto sNode : node->sameLevel) {
                    if (curr == sNode) { isFound = true; } }
                if (!isFound) {
                    node->sameLevel.push_back(curr);
                    curr->sameLevel.push_back(node); }
            }

            // If Node has Smaller Level than Current Node,
            // Set this Node as the Parent of the Current Node
            else if (node->level < curr->level) {
                for (auto pNode : curr->parents) {
                    if (node == pNode) { isFound = true; } }
                if (!isFound) { curr->addParent(node); }
            }
        }
    }

    // Step 3 = Edge Labelling

    // Iterate Over All Root Node Children
    EdgeStd bet;
    for (auto cNode : tree->children) {
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

    // Delete All Nodes (Dynamic Memory)
    for (auto dNode : deleteHelper) { delete dNode; }
    for (auto dNode : deleteHelperSmall) { delete dNode; }

}

// Inputs:
// G = Our Graph
// Output
// Edges = The Betweenness of all Edges
EdgeStd calculateBetweenness(Graph& G) {

    // The Betweenness of Graph
    EdgeStd betweenness;

    // Get Property Map for Vertices, Iterate, Pass Index to Function
    // Calculate Betweenness for all Paths from that Node
    IndexMap index = get(boost::vertex_index, G);
    for (auto n = vertices(G); n.first != n.second; ++n.first) {
        SSSP(G, index[*n.first], betweenness);
    }

    return betweenness;

}

// Input:
// G = Our Graph
// Node = Specified Node
// Visited = Already Visited Nodes
void findCommunities(Graph& G, unsigned long node, std::vector<unsigned long>& visited) {

    // Iterate over all Adjacent Nodes and Add Them to Visited Nodes
    auto neighbors = boost::adjacent_vertices(node, G);
    for (auto nNode : make_iterator_range(neighbors)) {

        // If Node hasn't been Visited, Add to Community and Visit Neighbors
        bool isFound = false;
        for (auto vNode : visited) {
            if (nNode == vNode) {
                isFound = true;
                break;
            }
        }
        if (!isFound) {
            visited.push_back(nNode);
            findCommunities(G, nNode, visited);
        }
    }
}

// Use the Normal Q value to
// Stop Loop when Removing

// Inputs:
// G = Our Graph
// Outputs:
// G = New Graph (Removed Edges)
Graph normalLoop(Graph& G) {

    // Iterate Until Q Value isn't Increasing
    float Q_prev = FLT_MIN;
    float Q = FLT_MIN;
    int i = 1;
    std::vector<std::tuple<unsigned long, unsigned long>> maxBetweenness;

    // Graph copy
    Graph OG;

    // Update Q_prev Value
    while (Q + 0.05 >= Q_prev) {

        Q_prev = Q;

        // Calculate Betweenness of All Edges in Graph
        auto betweenness = calculateBetweenness(G);

        // If Betweenness Empty, Break Loop
        if (betweenness.empty()) { break; }

        // Get Max Betweenness
        float maxBet = -1;
        for (auto kvPair : betweenness) {
            if (kvPair.second > maxBet) {
                maxBet = kvPair.second;
            }
        }

        // Find Edges with Greater Betweenness
        for (auto kvPair : betweenness) {
            if (kvPair.second >= maxBet / 2) {
                maxBetweenness.emplace_back(kvPair.first);
            }
        }

        // Store Number of Edges Before Removing
        auto numEdges = betweenness.size();

        // Copy Graph
        OG = Graph();
        boost::copy_graph(G, OG);

        // Remove all Max Edges from Graph
        for (auto b : maxBetweenness) {
            boost::remove_edge(std::get<0>(b), std::get<1>(b), G);
        }

        std::cout << "Iters: " << i << ", Removes: " << maxBetweenness.size() << std::endl;

        // Compute the modularity (Q)

        float sum1 = 0;
        float sum2 = 0;

        // Iterate over Nodes in Old Graph (OG)
        IndexMap indexOld = get(boost::vertex_index, OG);
        for (auto nOld = vertices(OG); nOld.first != nOld.second; ++nOld.first) {
            auto nOldNeighbors = boost::adjacent_vertices(indexOld[*nOld.first], G);

            // Number of Neighbors to nOld
            int oldNeighborAmount = 0;
            for (auto noVal : make_iterator_range(nOldNeighbors)) { ++oldNeighborAmount; }

            // Find the Communities Associated with Node
            std::vector<unsigned long> communities;
            findCommunities(G, indexOld[*nOld.first], communities);

            // Iterate over Nodes in New Graph (G)
            IndexMap indexNew = get(boost::vertex_index, G);
            for (auto nNew = vertices(G); nNew.first != nNew.second; ++nNew.first) {
                auto nNewNeighbors = boost::adjacent_vertices(indexNew[*nNew.first], G);

                // Number of Neighbors to nNew
                int newNeighborAmount = 0;
                for (auto noVal : make_iterator_range(nNewNeighbors)) { ++newNeighborAmount; }

                // Find Number of Edges Between Old and New
                int amountBet = 0;
                for (auto adjNeighbor : make_iterator_range(nOldNeighbors)) {
                    if (adjNeighbor == indexNew[*nNew.first]) {
                        amountBet = 1;
                        break;
                    }
                }

                // Getting B
                float B = (float)amountBet - ((float)(oldNeighborAmount * newNeighborAmount) / (float)(numEdges * 2));

                // Calculate s Value (s_i * s_j) + 1
                int s = -1;
                for (unsigned long c : communities) {

                    // Is nNew in Same Community as nOld?
                    if (c == indexNew[*nNew.first]) {
                        s = 1;
                        break;
                    }
                }

                s++;

                // Compute Final B values for Iteration
                float B_1 = B * s;
                float B_2 = B;

                // Sum B values
                sum1 += B_1;
                sum2 += B_2;

            }
        }

        // Compute the Final Q Value
        Q = (1 / (2 * (float)numEdges)) * (0.5 * sum1 - sum2);

        // Print Values, Increment
        std::cout << "Modularity: " << Q << std::endl << std::endl;
        i += 1;

    }

    return OG;

}

// Handles Main Graph ( PrintGraph(G); )
// Argument: [File Path] [Name String]
// Example: data/football/football.graphml value
// Example: data/dataset.graphml community
int main(int argc, char* argv[]) {
    if (argc >= 3) {

        // Read in Graph
        std::ifstream I(argv[1]);
        Graph G = ReadGraph(I, argv[2]);

        // Copy Graph
        Graph OrigGraph;
        OrigGraph = Graph();
        boost::copy_graph(G, OrigGraph);

        // Remove Edges from Graph to get Communities
        G = normalLoop(G);

        // Iterate over Nodes and Find Communities
        std::vector<std::vector<unsigned long>> communities;
        std::vector<unsigned long> totalVisited;

        IndexMap index = get(boost::vertex_index, G);
        for (auto node = vertices(G); node.first != node.second; ++node.first) {
            auto itrNode = index[*node.first];

            // If Node has been Visited, Skip Iteration
            bool inTotalVisited = false;
            for (auto testNode : totalVisited) {
                if (itrNode == testNode) { inTotalVisited = true; } }
            if (inTotalVisited) { continue; }

            // Add Visited Nodes to Communities
            std::vector<unsigned long> visited;
            findCommunities(G, itrNode, visited);

            std::vector<unsigned long> pushTemp{itrNode};
            if (!visited.empty()) { communities.push_back(visited); }
            else { communities.push_back(pushTemp); }

            // Add Visited Nodes to Total Visited Nodes
            for (auto aNode : visited) {
                totalVisited.push_back(aNode);
            }
        }

        // Graphing

        std::vector<unsigned long> leftovers;

        // Put all Leftover Nodes (Nodes Without Class) Into Same Class
        for (auto community : communities) {
            if (community.size() == 1) {
                leftovers.push_back(community[0]);
            }
        }

        // Store Leftovers in Main List
        for (auto leftover : leftovers) {
            for (int i = 0; i < communities.size(); ++i) {
                if (communities[i][0] == leftover) {
                    communities.erase(communities.begin() + i);
                }
            }
        }

        if (!leftovers.empty()) { communities.push_back(leftovers); }

        // Print the Classes
        std::cout << "\n\n";
        for (int i = 0; i < communities.size(); ++i) {
            std::cout << "Class " << i << ": ";
            for (auto j : communities[i]) {
                if (j == communities[i][communities[i].size() - 1]) { break; }
                std::cout << j << ", "; }
            std::cout << communities[i][communities[i].size() - 1] << std::endl;
        }


        // Write Graph to File
//        std::ofstream O("output/output.graphml");
//        boost::dynamic_properties D(boost::ignore_other_properties); // Dynamic Properties
//        boost::write_graphml(std::cout, G, D);

        // Implement This:
        // # Print the classes
        //    print("\n\n")
        //    for c in range(0, len(comm)):
        //        print(f"Class {c}: ", end="")
        //        for v in comm[c][:-1]:
        //            print(v, end=", ")
        //        print(comm[c][-1])
        //
        //    # Get the communities for each node
        //    y_communities = dict()
        //    for n in orig._node.keys():
        //        try:
        //            y_communities[orig._node[n][commName]].append(n)
        //        except KeyError:
        //            y_communities[orig._node[n][commName]] = [n]
        //
        //    # Convert the dictionary to a list
        //    y = [i for i in y_communities.values()]
        //
        //    # Calculate the accuracy
        //    acc = calculateAccuracy(comm, y) = FIXME Need to Code
        //
        //    # Display the accuracy
        //    print(f"Accuracy: {acc}")

    } else { std::cout << "なに ですか？ Err: Provide Program Argument (Graphml Path)"; }
}

// Python Cross-Functionality (Abandoned)
// Py_Initialize(); // Initialize Environment
// PyRun_SimpleString("import sys"); // Call Import
// PyRun_SimpleString("sys.path.append('/src/dataGenerator.py')");
// Py_Finalize(); // End Environment

// Get Random Colors to Classify Every Node (Abandoned)
// char hex[6];
// char hex_char[]={'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
// srand(time(nullptr));
// hex[0] = '#';
// for (int i = 1; i <= 6; ++i) {
//      hex[i] = hex_char[rand() % 16]; }
// std::vector<char*> colormap;
// for (auto node : G) {