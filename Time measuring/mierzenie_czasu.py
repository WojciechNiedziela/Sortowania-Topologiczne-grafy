import argparse, os, re, sys
import Graph_class_time as Graph_class_time # type: ignore

sys.setrecursionlimit(1000000000)

Graph = Graph_class_time.Graph

def load_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        graph_type = lines[0].strip()  # Graph type
        nodes = int(lines[1].strip())  # Number of nodes
        graph = Graph(nodes, graph_type)
        for i in range(2, nodes+2):  # Nodes and their neighbors
            successors = list(map(int, lines[i].split()))
            graph.add_edge(i-1, successors)
        action1 = lines[nodes+2].strip()  # Command 1
        action2 = lines[nodes+3].strip()  # Command 2
    return graph, action1, action2


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-folder', default='data')
    args = parser.parse_args()

    data_folder = args.data_folder
    files = os.listdir(data_folder)
    files = sorted(files, key=lambda f: int(re.search(r'file(\d+)', f).group(1)))

    for filename in files:
        file_path = os.path.join(data_folder, filename)
        graph, action1, action2 = load_graph_from_file(file_path)
        print(f"Loaded graph from {filename}:")
        # print(graph.graph)

        if action1 == "tarjan":
            graph.reset_visited()  # Reset visited list before running Tarjan's algorithm
            start_node = graph.find_start_node()
            if start_node is None:
                print("The graph contains a cycle.")
            else:
                graph.tarjan(start_node)  # Run Tarjan's algorithm
                graph.sccs.reverse()
                # print('[', end='')
                # for scc in graph.sccs:
                #     print(*scc, end="" + ', ' if scc != graph.sccs[-1] else '')
                # print(']')
        # Add more actions as needed...

if __name__ == "__main__":
    main()