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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    args = parser.parse_args()

    if args.generate:
        nodes = int(input("Podaj liczbę węzłów: "))
        saturation = float(input("Podaj nasycenie (jako ułamek od 0 do 1): "))

        dag = generate_dag(nodes, saturation)
        print("Wygenerowana macierz sąsiedztwa DAG:")
        print(dag)

if __name__ == "__main__":
    main()
