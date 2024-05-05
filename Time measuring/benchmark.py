import os
import random

def generate_dag_data(n):
    data = []
    for i in range(1, n+1):
        possible_neighbors = list(range(i+2, n+1))  # Exclude the node itself
        edges = random.sample(possible_neighbors, min(random.randint(0, len(possible_neighbors)), n-i))
        data.append((i, edges))
    return data

# def create_dag_files(start, end, step):
#     for num_nodes in range(start, end+1, step):
#         with open(os.path.join('Sortowania-Topologiczne-grafy/Time measuring/data', f'dag_file{num_nodes}.txt'), 'w') as f:
#             f.write("matrix\n")  # Graph type
#             f.write(str(num_nodes) + '\n')  # Number of nodes
#             dag_data = generate_dag_data(num_nodes)  # Generate DAG data
#             for node, edges in dag_data:
#                 f.write(str(node) + ' ' + ' '.join(map(str, edges)) + '\n')  # Nodes and their neighbors
#                 # f.write(' '.join(map(str, edges)) + '\n')  # Nodes and their neighbors
#             f.write("tarjan\n")  # Last line
#             f.write("exit\n")  # Last line


def create_dag_files(start, end, step):
    for num_nodes in range(start, end+1, step):
        with open(os.path.join('Sortowania-Topologiczne-grafy/Time measuring/data', f'dag_file{num_nodes}.txt'), 'w') as f:
            f.write("matrix\n")  # Graph type
            f.write(str(num_nodes) + '\n')  # Number of nodes
            dag_data = generate_dag_data(num_nodes)  # Generate DAG data
            for node, edges in dag_data:
                f.write(' '.join(map(str, edges)) + '\n')  # Nodes and their neighbors
            f.write("tarjan\n")  # Last line
            f.write("exit\n")  # Last line

os.makedirs('Sortowania-Topologiczne-grafy/Time measuring/data', exist_ok=True)

create_dag_files(pow(2, 2), pow(2, 4), 2)
