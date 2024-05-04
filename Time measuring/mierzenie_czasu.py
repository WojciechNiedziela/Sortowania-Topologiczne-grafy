import argparse
import Graph_class_time as Graph_class_time # type: ignore

Graph = Graph_class_time.Graph


def generate_dag(nodes, saturation): # Dag - Directed Acyclic Graph
    graph = Graph(nodes, "list")  # We'll use an adjacency list to represent the DAG

    # Add edges to the graph
    for i in range(1, nodes+1): # For each node
        edges = []
        for j in range(i+1, min(i+1+int(nodes*saturation), nodes+1)): # Add edges to the next nodes depending on the saturation
            edges.append(j) # Add an edge to the next node
        graph.add_edge(i, edges) # Add the edges to the graph

    return graph

def load_user_provided_graph(): # Load a user-provided graph (ask for data)

    valid_types = ["matrix", "list", "table"]
    graph_type = ""

    while graph_type not in valid_types:
        graph_type = input("type> ").lower()
        if graph_type not in valid_types:
            print("Invalid type. Please enter either 'matrix', 'list', or 'table'.")

    nodes = int(input("Nodes> "))
    graph = Graph(nodes, graph_type)

    for i in range(1, nodes+1):
        successors = list(map(int, input(f"{i}> ").split()))
        graph.add_edge(i, successors)

    return graph_type, graph

def display_help(): # Display help
    print("Available commands:")
    print("help     -   display help")
    print("dfs      -   perform Depth-First Search on the graph")
    print("tarjan   -   perform Tarjan's algorithm on the graph")
    print("export   -   export the graph to a LaTeX file")
    print("exit     -   exit the program")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--generate2', action='store_true')
    parser.add_argument('--user-provided', action='store_true')
    args = parser.parse_args()

    graph = None
    if args.generate:
        nodes = int(input("Nodes> "))
        saturation = float(input("Saturation> "))/100

        graph = generate_dag(nodes, saturation)  # Generate a directed acyclic graph (DAG)
        print("Generated graph:")
        print(graph.graph)  # Display the graph
        
    elif args.user_provided:
        graph_type, graph = load_user_provided_graph()
        print(f"Graph representation: {graph_type}")
        print("User-provided graph:")
        print(graph.graph)

    while True:
        command = input("> ").lower()
        if command == "dfs":
            if graph is not None:
                graph.reset_visited()  # Reset visited list before running DFS
                print("Depth-First Search:")
                print(graph.dfs_all())
            else:
                print("No graph to perform DFS on.")
        elif command == "tarjan":
            if graph is not None:
                graph.reset_visited()  # Reset visited list before running Tarjan's algorithm
                start_node = graph.find_start_node()
                if start_node is None:
                    print("The graph contains a cycle.")
                else:
                    graph.tarjan(start_node)  # Run Tarjan's algorithm
                    graph.sccs.reverse()
                    print('[', end='')
                    for scc in graph.sccs:
                        print(*scc, end="" + ', ' if scc != graph.sccs[-1] else '')
                    print(']')
                    
            else:
                print("No graph to perform Tarjan's algorithm on.")
        elif command == "export":
            if graph is not None:
                with open("graph.tex", "w") as tex_file:
                    graph.export(tex_file)
                print("Graph exported to graph.tex.")
            else:
                print("No graph to export.")
        elif command == "help":
            display_help()
        elif command == "exit":
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
