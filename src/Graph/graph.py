import math
import os
from queue import Queue
import heapq

import networkx as nx  # type: ignore
import matplotlib.pyplot as plt
from networkx import reconstruct_path  # type: ignore # idem
from pyvis.network import Network  # type: ignore

from .node import Node
from Types.area import Area

import pandas as pd # type: ignore
import ast

import random

from Types.supply import Supply

from adjustText import adjust_text # type: ignore

from Types.veicule import Vehicle

class Graph:
    def __init__(self, directed= False):
        self.nodes = []
        self.directed = directed
        self.graph = {}
        self.conections = {}

    def calculate_distance(self,lat1, lon1, lat2, lon2):

        R = 6371  # Radius of Earth in kilometers
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in kilometers

    def getGraphTuple(self, node):
        return self.graph[node]

    def getGraph(self):
        return self.graph

    def calculate_cost(self, path: list):
        if len(path) < 2:
            return 0 

        cost = 0
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]

            edges = self.graph.get(node1, [])
            for neighbor, weight in edges:
                if neighbor == node2:
                    if weight == -1:
                        return float('inf') 
                    cost += weight
                    break
            else:
                print(f"Erro: Sem conexÃ£o entre {node1} e {node2}")
                return float('inf')

        return cost


    def add_edge(self, node1, node2):
        n1: Node = self.get_node_by_name(node1)
        n2: Node = self.get_node_by_name(node2)

        if n1 is None:
            print(f"Erro: nodo {node1} nao encontrado!")
            return  

        if n2 is None:
            print(f"Erro: nodo {node2} nao encontrado!")
            return  
        
        if n1 not in self.nodes:
            n1_id = len(self.nodes)
            n1 = Node(n1_id, n1.getArea(), n1.getNeeds())
            self.nodes.append(n1)
            self.graph[node1] = []

        if n2 not in self.nodes:
            n2_id = len(self.nodes) 
            n2 = Node(n2_id, n2.getArea(), n2.getNeeds())  
            self.nodes.append(n2)
            self.graph[node2] = []

        if random.random() < 0.05:  # 5% de chance para peso infinito
            weight = weight = -1 # rep do infinito
        else:

            weight = self.calculate_distance(n1.getLatitude(), n1.getLongitude(), n2.getLatitude(), n2.getLongitude())

        self.graph[node1].append((node2, weight))


    def get_node_by_name(self, name):
        search_node = name
        for node in self.nodes:
            if node.getName() == search_node:
                return node
        return None

    def parse_supplies(self):
        supplies_data = {}

        # Lê os dados diretamente dos arquivos CSV na mesma pasta que o main.py
        food_df = pd.read_csv("food.csv")
        medicine_df = pd.read_csv("medicine.csv")
        equipment_df = pd.read_csv("equipment.csv")

        # Processa os dados do CSV "food.csv"
        supplies_data['Food'] = [
            (row['Comida'], row['PesoPack'], math.inf if row['ShelfLife'] == 'inf' else row['ShelfLife'])
            for _, row in food_df.iterrows()
        ]

        # Processa os dados do CSV "medicine.csv"
        supplies_data['Medicine'] = [
            (row['Medicamento'], row['PesoPack'], math.inf if row['ShelfLife'] == 'inf' else row['ShelfLife'])
            for _, row in medicine_df.iterrows()
        ]

        # Processa os dados do CSV "equipment.csv"
        supplies_data['Equipment'] = [
            (row['Equipamento'], row['PesoPack'], math.inf)
            for _, row in equipment_df.iterrows()
        ]

        return supplies_data
    
    def createGraph(self, supplies_data):
        df = pd.read_csv("map.csv")

        for _, row in df.iterrows():
            country = row['Country']
            latitude = row['Latitude']
            longitude = row['Longitude']
            population = row['Population']
            region = row['Region']
            accessibility = row['AccessibilityIndex']
            criticalTime = random.randint(2000, 10080)

            weather = random.randint(1, 10)
            area = Area(country, population, weather, accessibility, region, criticalTime, longitude, latitude)

            supplyTypeNum = random.randint(1, 4)
            supplies = []
            afected = random.choice([True,False])

            if afected is True: 
                for i in range(supplyTypeNum):
                    supply_type = random.choice(list(supplies_data.keys()))
                    supply_info = random.choice(supplies_data[supply_type])
                    supply_name = supply_info[0]
                    supply_weight = supply_info[1]
                    supply_quantity = random.randint(30, 100)
                    supply_shelf_life = supply_info[2]

                    supply = Supply(supply_type, supply_name, supply_weight, supply_quantity, supply_shelf_life)
                    supplies.append(supply)


            node_id = len(self.nodes)
            node = Node(node_id, area, supplies, afected)
            self.nodes.append(node)
            self.graph[country] = []

        for _, row in df.iterrows():
            country = row['Country']
            adjacents = ast.literal_eval(row['Adjacentes'])

            for adjacent in adjacents:
                adjacent_country = adjacent[0]
                connection_type = adjacent[1]
                
                self.conections[(country,adjacent_country)] = connection_type

                self.add_edge(country, adjacent_country)


    def draw(self, output_path='graph.png'):
        lista_v = self.nodes
        g = nx.Graph()
        node_colors = []
        node_labels = {}

        for nodo in lista_v:
            n = nodo.getName()
            afected = getattr(nodo, 'afected', False)
            heuristic = round(nodo.getHeuristic(), 1)  
            g.add_node(n)

            node_colors.append('red' if afected else 'lightblue')  
            node_labels[n] = f"{n}\nH: {heuristic}"

            # Iterar sobre os adjacentes de cada nodo
            for adjacente, peso in self.graph[n]:
                g.add_edge(n, adjacente, weight=round(peso, 2)) 

        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(g, seed=42, k=2, weight='weight') 

        nx.draw_networkx_nodes(
            g, pos, node_size=300, node_color=node_colors, edgecolors='black'
        )
        nx.draw_networkx_edges(g, pos, edge_color='gray', alpha=0.7, width=1.2)

        nx.draw_networkx_labels(g, pos, labels=node_labels, font_size=7, font_color='black', font_weight='bold')

        edge_labels = {}

        for nodo in lista_v:
          n = nodo.getName()
          for adjacente, peso in self.graph[n]:
              
            connection_type = self.conections.get((n, adjacente), 'Unknown')

            if peso == -1:
                edge_labels[(n, adjacente)] = f"{-1} ({connection_type})" 
            else:
                edge_labels[(n, adjacente)] = f"{round(peso, 2)} ({connection_type})"

        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=6, label_pos=0.5)

        plt.title("Grafo", fontsize=15)
        plt.axis('off')
        plt.tight_layout()

        plt.savefig(output_path, format='png')
        plt.close()
    
    
    
    def update_grafo(self, traveltime):
        nodesList = self.nodes
    
        for node in nodesList:
            if(node.afected == True):
                node.updateCriticalTime(traveltime)
                node.updatePriority()

    #FUNÇAO SUPPLY DE VEICULO 

    def procura_DFS(self, start, end, path, visited, vehicle: Vehicle):
        path.append(start)
        visited.add(start)

        if start == end:

            custoT = self.calculate_cost(path)
            return path, custoT

        for adjacente, _ in self.graph[start]:
            if adjacente not in visited:
                distance = self.calculate_distance(
                    self.nodes[start].area.latitude, self.nodes[start].area.longitude,
                    self.nodes[adjacente].area.latitude, self.nodes[adjacente].area.longitude
                )
                
                time = vehicle.calculateTravelTime(distance)

                self.update_grafo(time)
                
                success = vehicle.updatevehicle(distance)
                if not success:
                    return None

                resultado = self.procura_DFS(adjacente, end, path, visited, vehicle)
                if resultado is not None:
                    return resultado

        path.pop()
        return None

    def procura_BFS(graph, start, end, direction):
        visited = set()
        fila = Queue()
        custo = 0
        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False

        while not fila.empty() and not path_found:
            nodo_atual = fila.get()

            if direction == 'forward':
                neighbors = graph.graph[nodo_atual] 
            elif direction == 'backward':
                neighbors = [(adjacente, peso) for adjacente, peso in graph.getNeighbours(nodo_atual) 
                             if nodo_atual in [adj[0] for adj in graph.graph[adjacente]]]

            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in neighbors:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            custo = graph.calculate_cost(path)
        return (path, custo)


    def getNeighbours(graph, nodo):
        lista = []
        for (adjacente, peso) in graph.graph[nodo]:
            lista.append((adjacente, peso))
        return lista
    
    def reconstruct_path(visited, start, end):
        path = []
        current = end 
        while current is not None:
            path.append(current) 
            current = visited[current][1]

        path.reverse()
        return path

    def procura_custo_uniforme(self, start, end):
        priority_queue = [(0, start)] 
        visited = {start: (0, None)} 

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                path = self.reconstruct_path(visited, start, end)
                return current_cost, path

            for neighbor, cost in self.graph.get(current_node, []):
                if cost == -1: 
                    continue

                total_cost = current_cost + cost

                if neighbor not in visited or total_cost < visited[neighbor][0]:
                    visited[neighbor] = (total_cost, current_node)
                    heapq.heappush(priority_queue, (total_cost, neighbor))

        return float('inf'), []
    
    #### informados

    def greedy(graph, start, end):
        open_list = set([start])
        closed_list = set([])

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or graph.graph[v].getHeuristic() < graph.graph[v].getHeuristic():
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                return (reconst_path, graph.calculate_cost(reconst_path))

            for (m, weight) in graph.getNeighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def procura_aStar(graph, start, end):
        open_list = {start}
        closed_list = set([])

        g = {}
        g[start] = 0

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or g[v] + graph.graph[v].getHeuristic() < g[n] + graph.graph[v].getHeuristic():
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                return (reconst_path, graph.calculate_cost(reconst_path))

            for (m, weight) in graph.getNeighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None