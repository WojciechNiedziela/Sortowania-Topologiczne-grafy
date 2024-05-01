import numpy as np
import argparse, math

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.graph = {i: [] for i in range(1, nodes+1)}
        self.visited = [False] * (nodes + 1)
        self.stack = []
        self.low_link = [0] * (nodes + 1)
        self.on_stack = [False] * (nodes + 1)
        self.time = 0
        self.sccs = []

    def add_edge(self, node, edges):
        self.graph[node] = edges

    def tarjan(self, node):
        self.low_link[node] = self.time
        self.visited[node] = self.time
        self.time += 1
        self.stack.append(node)
        self.on_stack[node] = True

        for neighbor in self.graph[node]:
            if not self.visited[neighbor]:
                self.tarjan(neighbor)
                self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
            elif self.on_stack[neighbor]:
                self.low_link[node] = min(self.low_link[node], self.visited[neighbor])

        if self.low_link[node] == self.visited[node]:
            scc = []
            while True:
                w = self.stack.pop()
                scc.append(w)
                self.on_stack[w] = False
                if w == node:
                    break
            self.sccs.append(scc)

    def dfs(self, node):
        if self.visited[node]:
            return []
        self.visited[node] = True
        nodes = [node]
        for neighbor in self.graph[node]:
            nodes += self.dfs(neighbor)
        return nodes

    def export(self, tex_file):
        tex_file.write("\\documentclass{standalone}\n")
        tex_file.write("\\usepackage{tikz}\n")
        tex_file.write("\\begin{document}\n")
        tex_file.write("\\begin{tikzpicture}[->,>=stealth]\n")

        # Liczba wierzchołków
        num_nodes = len(self.graph)

        # Promień okręgu (wielokrotność liczby wierzchołków)
        radius = num_nodes * 0.5

        # Wierzchołki na okręgu
        for i, node in enumerate(self.graph.keys()):
            angle = 2 * math.pi * i / num_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            tex_file.write(f"    \\node ({node}) at ({x},{y}) {{{node}}};\n")

        # Krawędzie
        for node, edges in self.graph.items():
            for edge in edges:
                if node == edge:  # Check if there is a connection to the same node
                    tex_file.write(f"    \\draw ({node}) edge [out=45, in=135, distance=1cm] ({node});\n")
                else:
                    tex_file.write(f"    \\draw ({node}) -- ({edge});\n")

        tex_file.write("\\end{tikzpicture}\n")
        tex_file.write("\\end{document}\n")




def generate_user_graph():
    graph_type = input("type> ")
    nodes = int(input("nodes> "))
    graph = Graph(nodes)

    for i in range(1, nodes+1):
        edges = list(map(int, input(f"{i}> ").split()))
        graph.add_edge(i, edges)

    return graph_type, graph

def generate_dag(nodes, saturation): # Dag - Directed Acyclic Graph
    # Tworzymy pustą macierz sąsiedztwa
    adjacency_matrix = np.zeros((nodes, nodes))

    # Wypełniamy górny trójkąt macierzy sąsiedztwa jedynkami
    for i in range(nodes):
        for j in range(i+1, min(i+1+int(nodes*saturation), nodes)):
            adjacency_matrix[i, j] = 1

    return adjacency_matrix

def load_user_provided_graph():
    nodes = int(input("Nodes> "))
    adjacency_list = []
    for i in range(1, nodes+1):  # Zmieniamy zakres na 1 do nodes+1
        successors = list(map(int, input(f"Podaj następników dla wierzchołka {i}: ").split()))
        adjacency_list.append(successors)
    return adjacency_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--generate2', action='store_true')
    parser.add_argument('--user-provided', action='store_true')
    args = parser.parse_args()

    graph = None
    if args.generate:
        graph_type, graph = generate_user_graph()
        print(f"Reprezentacja grafu: {graph_type}")
        print(f"Graf: {graph.graph}")
    elif args.generate2:
        nodes = int(input("Nodes> "))
        saturation = float(input("Saturation> "))/100

        dag = generate_dag(nodes, saturation)
        print("Wygenerowana macierz sąsiedztwa DAG:")
        print(dag)
    elif args.user_provided:
        graph = load_user_provided_graph()
        print("Wczytany graf od użytkownika:")
        print(graph)

    while True:
        command = input("> ").lower()
        if command == "dfs":
            if graph is not None:
                print("Przeszukiwanie w głąb:")
                print(graph.dfs(1))
            else:
                print("Brak grafu do przeszukania.")
        elif command == "tarjan":
            if graph is not None:
                for i in range(1, graph.nodes+1):
                    if not graph.visited[i]:
                        graph.tarjan(i)
                print("Silnie spójne składowe:")
                print(graph.sccs)
            else:
                print("Brak grafu do przeszukania.")
        elif command == "export":
            if graph is not None:
                with open("graph.tex", "w") as tex_file:
                    graph.export(tex_file)
                print("Graf został wyeksportowany do pliku graph.tex.")
            else:
                print("Brak grafu do wyeksportowania.")
        elif command == "help":
            print("help -   wyświetla pomoc\n")
            print("dfs  -   przechodzi graf przy pomocy algorytmu dfs\n")
            print("tarjan -   przechodzi graf przy pomocy algorytmu tarjana\n")
            print("export -   eksportuje graf do pliku LaTeX\n")
            print("exit -   wychodzi z programu\n")
        elif command == "exit":
            break
        else:
            print("Nieznane polecenie.")

if __name__ == "__main__":
    main()
