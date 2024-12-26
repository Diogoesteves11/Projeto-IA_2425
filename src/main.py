from Graph.graph import Graph
from Graph.node import Node
from Types.veicule import Vehicle
from Interface.aidmatrix import *
from Algorithms.algs_handler import *
import time
import copy

def main():
    g = Graph()

    supplies_data = g.parse_supplies()
    g.createGraph(supplies_data)
        
    vehicles = Vehicle.parse_csv_to_vehicles()
    vehicles_list = list(vehicles.values()) 
    
    while True:
        display_menu()
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            print("Abrindo o grafo...")
            g.draw()
            
        elif choice == "2":
            start = input("Digita o nome do nó inicial: ")
            
            while True:
                display_algorithm_menu()
                algo_choice = input("Escolha o algoritmo: ")
                
                if algo_choice == "0":
                    break
                
                g_copy = copy.deepcopy(g)
                
                if algo_choice == "1":
                    print("Executando a Busca em Profundidade...")
                    search(g_copy, start, vehicles_list, 0)
                
                elif algo_choice == "2":
                    print("Executando Busca em Largura (BFS)...")
                    search(g_copy, start, vehicles_list, 1)
                
                elif algo_choice == "3":
                    print("Executando Busca de Custo Uniforme...")
                    search(g_copy, start, vehicles_list, 2)
                    
                elif algo_choice == "4":
                    print("Executando Busca em Aprofundamento Iterativo...")
                    search(g_copy, start, vehicles_list, 3)
                
                elif algo_choice == "5":
                    print("Executando Greedy...")
                    search(g_copy, start, vehicles_list, 4)
                
                elif algo_choice == "6":
                    print("Executando A*...")
                    search(g_copy, start, vehicles_list, 5)
                
                else:
                    print("Opção inválida. Tente novamente.")
                
                g = g_copy
                time.sleep(2)   
            
        elif choice == "0":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(2)


if __name__ == "__main__":
    main()
