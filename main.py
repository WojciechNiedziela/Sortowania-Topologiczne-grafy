import numpy as np
import argparse, math

class Graph:
    def __init__(self, nodes, graph_type):
        self.nodes = nodes
        self.graph_type = graph_type
        if graph_type == "matrix":
            self.graph = np.zeros((nodes+1, nodes+1))  # Initialize an adjacency matrix with zeros
        elif graph_type == "list":
            self.graph = {i: [] for i in range(1, nodes+1)}  # Initialize an adjacency list
        elif graph_type == "table":
            self.graph = []  # Initialize an edge table


        self.visited = [False] * (nodes + 1)  # Keep track of visited nodes during traversal
        self.stack = []  # Stack for Tarjan's algorithm
        self.low_link = [0] * (nodes + 1)  # Low link values for Tarjan's algorithm
        self.on_stack = [False] * (nodes + 1)  # Keep track of nodes on the stack in Tarjan's algorithm
        self.time = 0  # Time counter for Tarjan's algorithm

    def add_edge(self, node, edges):
        if self.graph_type == "matrix":
            for edge in edges:
                self.graph[node][edge] = 1  # Add an edge in the adjacency matrix
        elif self.graph_type == "list":
            self.graph[node] = edges  # Add edges in the adjacency list
        elif self.graph_type == "table":
            for edge in edges:
                self.graph.append((node, edge))  # Add an edge in the edge table
        else:
            raise ValueError(f"Unknown graph type: {self.graph_type}")

    def find_start_node(self):
        for node in range(1, self.nodes+1):
            if not self.visited[node]:
                if self.graph_type == "matrix":
                    if all(self.graph[other_node][node] == 0 for other_node in range(1, self.nodes+1)):
                        return node
                elif self.graph_type == "table":
                    if all(edge[1] != node for edge in self.graph):
                        return node
                else:
                    if all(node not in self.graph[other_node] for other_node in self.graph):
                        return node
        return None

    def tarjan(self, node):
        self.low_link[node] = self.time
        self.visited[node] = self.time
        self.time += 1
        self.stack.append(node)
        self.on_stack[node] = True

        if self.graph_type == "matrix":
            for neighbor in range(1, self.nodes+1):
                if self.graph[node][neighbor]:
                    if not self.visited[neighbor]:
                        self.tarjan(neighbor)
                        self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                    elif self.on_stack[neighbor]:
                        self.low_link[node] = min(self.low_link[node], self.visited[neighbor])
        elif self.graph_type == "table":
            for edge in self.graph:
                if edge[0] == node:
                    neighbor = edge[1]
                    if not self.visited[neighbor]:
                        self.tarjan(neighbor)
                        self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                    elif self.on_stack[neighbor]:
                        self.low_link[node] = min(self.low_link[node], self.visited[neighbor])
        else:
            for neighbor in self.graph[node]:
                if not self.visited[neighbor]:
                    self.tarjan(neighbor)
                    self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                elif self.on_stack[neighbor]:
                    self.low_link[node] = min(self.low_link[node], self.visited[neighbor])

        
        if self.low_link[node] == self.visited[node]:
            while True:
                w = self.stack.pop()
                print(w, end='' + ' ')
                self.on_stack[w] = False
                if w == node:
                    break
                else:
                    print(", ", end='')  # Print a comma between elements
                    
    def export(self, tex_file):
        tex_file.write("\\documentclass{standalone}\n")
        tex_file.write("\\usepackage{tikz}\n")
        tex_file.write("\\begin{document}\n")
        tex_file.write("\\begin{tikzpicture}[->,>=stealth]\n")

        # Number of nodes
        num_nodes = self.nodes  # Use self.nodes instead of len(self.graph)

        # Radius of the circle (multiple of the number of nodes)
        radius = num_nodes * 0.5

        # Nodes on the circle
        for i in range(1, num_nodes+1):
            angle = 2 * math.pi * i / num_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            tex_file.write(f"    \\node ({i}) at ({x},{y}) {{{i}}};\n")

    # Edges
        if self.graph_type == "matrix":
            for i in range(1, num_nodes+1):
                for j in range(1, num_nodes+1):
                    if self.graph[i][j]:
                        tex_file.write(f"    \\draw ({i}) -- ({j});\n")
        elif self.graph_type == "table":
            for edge in self.graph:
                tex_file.write(f"    \\draw ({edge[0]}) -- ({edge[1]});\n")
        else:
            for node, edges in self.graph.items():
                for edge in edges:
                    tex_file.write(f"    \\draw ({node}) -- ({edge});\n")

        tex_file.write("\\end{tikzpicture}\n")
        tex_file.write("\\end{document}\n")

    def reset_visited(self):
        self.visited = [False] * (self.nodes + 1)

    def dfs(self, node):
        if self.visited[node]:
            return []
        self.visited[node] = True
        nodes = [node]
        if self.graph_type == "matrix":
            for neighbor in range(1, self.nodes+1):
                if self.graph[node][neighbor] and not self.visited[neighbor]:
                    nodes += self.dfs(neighbor)
        elif self.graph_type == "table":
            for edge in self.graph:
                if edge[0] == node and not self.visited[edge[1]]:
                    nodes += self.dfs(edge[1])
        else:
            for neighbor in self.graph[node]:
                if not self.visited[neighbor]:
                    nodes += self.dfs(neighbor)
        return nodes

    def dfs_all(self):
        self.reset_visited()  # Reset visited list before running DFS
        nodes = []
        for node in range(1, self.nodes+1):
            if not self.visited[node]:
                nodes += self.dfs(node)
        return nodes


def generate_user_graph():
    valid_types = ["matrix", "list", "table"]
    graph_type = ""

    while graph_type not in valid_types:
        graph_type = input("type> ").lower()
        if graph_type not in valid_types:
            print("Invalid type. Please enter either 'matrix', 'list', or 'table'.")

    nodes = int(input("nodes> "))
    graph = Graph(nodes, graph_type)

    for i in range(1, nodes+1):
        edges = list(map(int, input(f"{i}> ").split()))
        graph.add_edge(i, edges)

    return graph_type, graph

def generate_dag(nodes, saturation): # Dag - Directed Acyclic Graph
    graph = Graph(nodes, "list")  # We'll use an adjacency list to represent the DAG

    # Add edges to the graph
    for i in range(1, nodes+1):
        edges = []
        for j in range(i+1, min(i+1+int(nodes*saturation), nodes+1)):
            edges.append(j)
        graph.add_edge(i, edges)

    return graph

def load_user_provided_graph():



    valid_types = ["matrix", "list", "table"]
    graph_type = ""

    while graph_type not in valid_types:
        graph_type = input("type> ").lower()
        if graph_type not in valid_types:
            print("Invalid type. Please enter either 'matrix', 'list', or 'table'.")

    nodes = int(input("Nodes> "))
    graph = Graph(nodes, graph_type)

    for i in range(1, nodes+1):
        successors = list(map(int, input(f"Enter successors for node {i}: ").split()))
        graph.add_edge(i, successors)

    return graph_type, graph

def display_help():
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
                    print("[ ", end='')
                    graph.tarjan(start_node)
                    print("]")

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
