import numpy as np
import argparse

def generate_dag(nodes, saturation):
    # Tworzymy pustą macierz sąsiedztwa
    adjacency_matrix = np.zeros((nodes, nodes))

    # Wypełniamy górny trójkąt macierzy sąsiedztwa jedynkami
    for i in range(nodes):
        for j in range(i+1, min(i+1+int(nodes*saturation), nodes)):
            adjacency_matrix[i, j] = 1

    return adjacency_matrix

def load_user_provided_graph():
    nodes = int(input("Podaj liczbę węzłów: "))
    adjacency_list = []
    for i in range(1, nodes+1):  # Zmieniamy zakres na 1 do nodes+1
        successors = list(map(int, input(f"Podaj następników dla wierzchołka {i}: ").split()))
        adjacency_list.append(successors)
    return adjacency_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--user-provided', action='store_true')
    args = parser.parse_args()

    if args.generate:
        nodes = int(input("Podaj liczbę węzłów: "))
        saturation = float(input("Podaj nasycenie (jako liczbe od 0 do 100)): "))/100

        dag = generate_dag(nodes, saturation)
        print("Wygenerowana macierz sąsiedztwa DAG:")
        print(dag)
    elif args.user_provided:
        graph = load_user_provided_graph()
        print("Wczytany graf od użytkownika:")
        print(graph)

if __name__ == "__main__":
    main()
