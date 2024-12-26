import os
import time

def display_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("========== AID MATRIX PRO+ ==========\n")
    print("1. Visualizar o grafo")
    print("2. Escolher o tipo de algoritmo")
    print("0. Sair")
    print("\n==================================")
    
def display_algorithm_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("======= ESCOLHER ALGORITMO =======\n")
    print("Algoritmos Não Informados:\n")
    print("1. Busca em Profundidade (DFS)")
    print("2. Busca em Largura (BFS)")
    print("3. Custo Uniforme")
    print("4. IDS")
    print("\nAlgoritmos Informados:\n")
    print("5. Greedy")
    print("6. A*")
    print("7. SMA*")
    print("\n------------------------------------\n")
    print("0. Voltar ao menu inicial")
    print("\n==================================")