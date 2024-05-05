import numpy as np
import math
import time

def timer_decorator(func):
    def wrapper(self, node, initial_call=True):
        if initial_call:
            wrapper._start_time = time.time()
        result = func(self, node, initial_call=False)
        if initial_call:
            wrapper._total_time = time.time() - wrapper._start_time
            with open('results.txt', 'a') as f:  # Open the file in append mode
                f.write(f"{wrapper._total_time}\n")  # Write the result to the file
        return result
    return wrapper





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


        self.visited = [False] * (nodes + 1)  # Keep track of visited nodes during traversal (DFS, Tarjan's algorithm)
        self.stack = []  # Stack for Tarjan's algorithm
        self.low_link = [0] * (nodes + 1)  # Low link values for Tarjan's algorithm, the smallest visited node reachable from the current node
        self.on_stack = [False] * (nodes + 1)  # Keep track of nodes on the stack in Tarjan's algorithm
        self.time = 0  # Time counter for Tarjan's algorithm -> used for assigning visited times to nodes (depth)
        self.sccs = []  # list with the results of Tarjan's algorithm
        # self._initial_call = True

    def add_edge(self, node, edges): # Add an edge to the graph
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

    def find_start_node(self): # Find a node with no incoming edges to use in topological sort
        for node in range(1, self.nodes+1): # Iterate over all nodes
            if not self.visited[node]: # If the node has not been visited
                if self.graph_type == "matrix":
                    if all(self.graph[other_node][node] == 0 for other_node in range(1, self.nodes+1)): # Check if there are no incoming edges
                        return node
                elif self.graph_type == "table":
                    if all(edge[1] != node for edge in self.graph): # Check if there are no incoming edges
                        return node
                else:
                    if all(node not in self.graph[other_node] for other_node in self.graph): # Check if there are no incoming edges
                        return node
        return None



    @timer_decorator
    def tarjan(self, node, initial_call=True): # Tarjan's algorithm for sorting topologically
        self.low_link[node] = self.time 
        self.visited[node] = self.time # Assign the visited time to the node
        self.time += 1
        self.stack.append(node) # Add the node to the stack
        self.on_stack[node] = True # Mark the node as being on the stack

        if self.graph_type == "matrix":
            for neighbor in range(1, self.nodes+1): 
                if self.graph[node][neighbor]: # If there is an edge
                    if not self.visited[neighbor]: # If the neighbor has not been visited
                        self.tarjan(neighbor, initial_call=False) # Perform Tarjan's algorithm on the neighbor
                        self.low_link[node] = min(self.low_link[node], self.low_link[neighbor]) # Update the low link value
                    elif self.on_stack[neighbor]: # If the neighbor is on the stack
                        self.low_link[node] = min(self.low_link[node], self.visited[neighbor]) # Update the low link value
        elif self.graph_type == "table":
            for edge in self.graph:
                if edge[0] == node:
                    neighbor = edge[1]
                    if not self.visited[neighbor]:
                        self.tarjan(neighbor, initial_call=False)
                        self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                    elif self.on_stack[neighbor]:
                        self.low_link[node] = min(self.low_link[node], self.visited[neighbor])
        else:
            for neighbor in self.graph[node]:
                if not self.visited[neighbor]:
                    self.tarjan(neighbor, initial_call=False)
                    self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                elif self.on_stack[neighbor]:
                    self.low_link[node] = min(self.low_link[node], self.visited[neighbor])

        if self.low_link[node] == self.visited[node]:
            scc = []  # Initialize a new strongly connected component
            while True:
                w = self.stack.pop()
                scc.append(w)  # Add the node to the strongly connected component
                self.on_stack[w] = False
                if w == node:
                    break
            self.sccs.append(scc)  # Add the strongly connected component to the list
                    
    def export(self, tex_file):     # Export the graph to a LaTeX file
        tex_file.write("\\documentclass{standalone}\n")
        tex_file.write("\\usepackage{tikz}\n")
        tex_file.write("\\begin{document}\n")
        tex_file.write("\\begin{tikzpicture}[->,>=stealth]\n")

        # Number of nodes
        num_nodes = self.nodes 

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
                        if i == j:  # Check if there is a connection to the same node
                            tex_file.write(f"    \\draw ({i}) edge [out=45, in=135, distance=1cm] ({i});\n")
                        else:
                            tex_file.write(f"    \\draw ({i}) -- ({j});\n")
        elif self.graph_type == "table":
            for edge in self.graph:
                if edge[0] == edge[1]:  # Check if there is a connection to the same node
                    tex_file.write(f"    \\draw ({edge[0]}) edge [out=45, in=135, distance=1cm] ({edge[0]});\n")
                else:
                    tex_file.write(f"    \\draw ({edge[0]}) -- ({edge[1]});\n")
        else:
            for node, edges in self.graph.items():
                for edge in edges:
                    if node == edge:  # Check if there is a connection to the same node
                        tex_file.write(f"    \\draw ({node}) edge [out=45, in=135, distance=1cm] ({node});\n")
                    else:
                        tex_file.write(f"    \\draw ({node}) -- ({edge});\n")

        tex_file.write("\\end{tikzpicture}\n")
        tex_file.write("\\end{document}\n")

    def reset_visited(self): # Reset visited list before running DFS
        self.visited = [False] * (self.nodes + 1)

    def dfs(self, node):    # Depth-First Search
        if self.visited[node]: # If the node has been visited, return an empty list
            return []
        self.visited[node] = True
        nodes = [node] # Initialize a list with the current node
        if self.graph_type == "matrix":
            for neighbor in range(1, self.nodes+1): # Iterate over all neighbors
                if self.graph[node][neighbor] and not self.visited[neighbor]: # If there is an edge and the neighbor has not been visited
                    nodes += self.dfs(neighbor) # Perform DFS on the neighbor
        elif self.graph_type == "table":
            for edge in self.graph:
                if edge[0] == node and not self.visited[edge[1]]: # If the edge starts at the current node and the neighbor has not been visited
                    nodes += self.dfs(edge[1]) # Perform DFS on the neighbor
        else:
            for neighbor in self.graph[node]:
                if not self.visited[neighbor]: # If the neighbor has not been visited
                    nodes += self.dfs(neighbor) # Perform DFS on the neighbor
        return nodes

    def dfs_all(self):  # Perform DFS on all nodes if not every nodes are connected
        self.reset_visited()  # Reset visited list before running DFS
        nodes = []
        for node in range(1, self.nodes+1): 
            if not self.visited[node]: # If the node has not been visited
                nodes += self.dfs(node) # Perform DFS on the node
        return nodes