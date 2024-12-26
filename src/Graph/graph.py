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
import Algorithms
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

    def getNodes(self):
        return self.nodes
    
    def get_random_node(self):
        nodes = self.getNodes()
        
        if not nodes:
            return None 

        random_node = random.choice(nodes)
        while random_node.getAffected() is not False:
            random_node = random.choice(nodes)
        node = random_node.getName()
        print(node)
        return node
    
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

        if random.random() < 0.01:  # 1% de chance para peso infinito
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
    
    def get_connection_type(self, node1, node2):
        connection = self.conections.get((node1, node2))
        if connection:
            return connection
        else:
            return f"Não há conexão entre {node1} e {node2}"
    
    def finish_travel(self, end):
        node = self.get_node_by_name(end)
        node.setAffected(False)
        area = node.getArea()
        area.setPriority(0)
        #print('Supplied: ' + end + '|| '+ str(node.getAffected()))

    def compatibleConection(self, start, end, vehicle: Vehicle):
        con = self.conections.get((start, end))
        if con is None: 
            return False

        if (vehicle.getvehicleType() == 'aquatico' and con == 0) or \
           (vehicle.getvehicleType() == 'terrestre' and con == 1): 
            return False

        return True
        
    
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
            refuel = False
            if not afected:
                refuel = random.choice([True,False])

            if afected is True: 
                for i in range(supplyTypeNum):
                    supply_type = random.choice(list(supplies_data.keys()))
                    supply_info = random.choice(supplies_data[supply_type])
                    supply_name = supply_info[0]
                    supply_weight = supply_info[1]
                    supply_quantity = random.randint(10, 30)
                    supply_shelf_life = supply_info[2]

                    supply = Supply(supply_type, supply_name, supply_weight, supply_quantity, supply_shelf_life)
                    supplies.append(supply)



            node_id = len(self.nodes)
            node = Node(node_id, area, supplies, afected, refuel)
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
        color_map = {}  # Mapeamento de nós para suas cores

        for nodo in lista_v:
            n = nodo.getName()
            afected = nodo.getAffected()
            refuel = nodo.getRefuel()
            heuristic = round(nodo.getHeuristic(), 1)  
            g.add_node(n)

            # Usar um dicionário para mapear o nó para sua cor
            color_map[n] = 'red' if afected else 'lightblue'  
            if refuel is True:
                color_map[n] = 'darkblue'
            node_labels[n] = f"{n}\nH: {heuristic}"

            # Iterar sobre os adjacentes de cada nodo
            for adjacente, peso in self.graph[n]:
                g.add_edge(n, adjacente, weight=round(peso, 2)) 

        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(g, seed=42, k=2, weight='weight') 

        # Criar lista de cores de acordo com a ordem dos nós no layout
        node_colors = [color_map[n] for n in g.nodes]

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

        plt.show()
        plt.close()
    
    def update_grafo(self, traveltime):
        for node in self.nodes:
            node_aux: Node = self.get_node_by_name(node)
            if node_aux is not None:
                if node_aux.getAffected() is True:
                    node_aux.updateCriticalTime(traveltime)
                    node_aux.updatePriority()
                for adjacente, w in self.graph[node]:
                    if random.random() < 0.01:  # 1% de chance para peso infinito
                        w = -1 # rep do infinito
                    else:
                        w = self.calculate_distance(node_aux.getLatitude(), node_aux.getLongitude(), adjacente.getLatitude(), adjacente.getLongitude())


    def procura_DFS(self, start, end, path, visited, vehicle: Vehicle):        
        path.append(start)
        visited.add(start)
        minimum = 0
        distance = 0
        needs = self.get_node_by_name(end).getNeeds()

        for need in needs:
            minimum += need.getSupplyWeightLoad()

        if start == end:
            custoT = self.calculate_cost(path)
            area = self.get_node_by_name(end)
            refuel = area.getRefuel()
            vehicle.updateVehicle(distance,needs, True, refuel)
            self.finish_travel(end)
            return path, custoT

        for adjacente, custo in self.graph[start]:
            if adjacente not in visited and self.compatibleConection(start, adjacente, vehicle) and custo !=  -1:
                distance = self.calculate_distance(
                    self.get_node_by_name(start).getLatitude(), self.get_node_by_name(start).getLongitude(),
                    self.get_node_by_name(adjacente).getLatitude(), self.get_node_by_name(adjacente).getLongitude()

                )
                time = vehicle.calculateTravelTime(distance)

                refuel = self.get_node_by_name(adjacente).getRefuel()
                self.update_grafo(time)
                if vehicle.updateVehicle(distance,needs,False, refuel) is False:
                    break

                area = self.get_node_by_name(adjacente).getArea()
                resultado = self.procura_DFS(adjacente, end, path, visited, vehicle)
                if resultado[1] is not float('inf'):
                    return resultado
        path.pop()
        return [], float('inf')

    def procura_BFS(self, start, end, vehicle): 
        visited = set()
        fila = Queue()

        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        minimum = 0
        distance = 0
        needs = self.get_node_by_name(end).getNeeds()

        for need in needs:
            minimum += need.getSupplyWeightLoad()

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
                area = self.get_node_by_name(end)
                refuel = area.getRefuel()
                vehicle.updateVehicle(distance,needs, True, refuel)
                self.finish_travel(end)
            else: 
                for (adjacente,peso) in self.graph[nodo_atual]:
                    if adjacente not in visited and self.compatibleConection(nodo_atual, adjacente, vehicle) and peso != -1:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)
                        distance = self.calculate_distance(
                            self.get_node_by_name(start).getLatitude(), self.get_node_by_name(start).getLongitude(),
                            self.get_node_by_name(adjacente).getLatitude(), self.get_node_by_name(adjacente).getLongitude()
                        )
                        time = vehicle.calculateTravelTime(distance)
                        refuel = self.get_node_by_name(adjacente).getRefuel()
                        self.update_grafo(time)
                        if vehicle.updateVehicle(distance,needs,False, refuel) is False:
                            break
                        self.update_grafo(time)
                
        
        path = []
        custoT = float('inf')
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            custoT = self.calculate_cost(path)
        return (path,custoT)


    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.graph[nodo]:
            lista.append((adjacente, peso))
        return lista
    
    def reconstruct_path(self,visited, start, end):
        path = []
        current = end 
        while current is not None:
            path.append(current) 
            current = visited[current][1]

        path.reverse()
        return path

    def procura_custo_uniforme(self, start, end, vehicle: Vehicle):
        priority_queue = [(0, start)] 
        visited = {start: (0, None)} 

        minimum = 0
        distance = 0
        needs = self.get_node_by_name(end).getNeeds()

        for need in needs:
            minimum += need.getSupplyWeightLoad()

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                path = self.reconstruct_path(visited, start, end)
                area = self.get_node_by_name(end)
                refuel = area.getRefuel()
                vehicle.updateVehicle(distance,needs, True, refuel)
                self.finish_travel(end)
                return path, current_cost

            for neighbor, cost in self.graph.get(current_node, []):
                if cost == -1: 
                    continue

                total_cost = current_cost + cost

                if neighbor not in visited or total_cost < visited[neighbor][0] and self.compatibleConection(current_node, neighbor, vehicle) and cost != -1:
                    visited[neighbor] = (total_cost, current_node)
                    heapq.heappush(priority_queue, (total_cost, neighbor))
                    distance = self.calculate_distance(
                        self.get_node_by_name(start).getLatitude(), self.get_node_by_name(start).getLongitude(),
                        self.get_node_by_name(neighbor).getLatitude(), self.get_node_by_name(neighbor).getLongitude()
                    )
                    time = vehicle.calculateTravelTime(distance)
                    refuel = self.get_node_by_name(neighbor).getRefuel()
                    self.update_grafo(time)
                    if vehicle.updateVehicle(distance,needs,False, refuel) is False:
                        break
                    self.update_grafo(time)

        return [], float('inf')
    
    def depth_limited_search(self, start, goal, depth_limit, vehicle: Vehicle):
        def dls_recursive(current, goal, depth, visited, path, vehicle):
            if depth < 0:
                return [], float('inf')
            
            path.append(current)
            visited.add(current)
            
            # Check if goal is reached
            if current == goal:
                custoT = self.calculate_cost(path)
                area = self.get_node_by_name(goal)
                refuel = area.getRefuel()
                
                # Get the distance for vehicle update
                if len(path) > 1:
                    distance = self.calculate_distance(
                        self.get_node_by_name(path[-2]).getLatitude(),
                        self.get_node_by_name(path[-2]).getLongitude(),
                        self.get_node_by_name(current).getLatitude(),
                        self.get_node_by_name(current).getLongitude()
                    )
                else:
                    distance = 0
                    
                needs = self.get_node_by_name(goal).getNeeds()
                vehicle.updateVehicle(distance, needs, True, refuel)
                self.finish_travel(goal)
                return path, custoT
            
            # Explore neighbors within depth limit
            for adjacente, custo in self.graph[current]:
                if (adjacente not in visited and 
                    self.compatibleConection(current, adjacente, vehicle) and 
                    custo != -1):
                    
                    # Calculate distance and update vehicle state
                    distance = self.calculate_distance(
                        self.get_node_by_name(current).getLatitude(),
                        self.get_node_by_name(current).getLongitude(),
                        self.get_node_by_name(adjacente).getLatitude(),
                        self.get_node_by_name(adjacente).getLongitude()
                    )
                    
                    time = vehicle.calculateTravelTime(distance)
                    refuel = self.get_node_by_name(adjacente).getRefuel()
                    self.update_grafo(time)
                    
                    needs = self.get_node_by_name(goal).getNeeds()
                    if vehicle.updateVehicle(distance, needs, False, refuel) is False:
                        continue
                    
                    result_path, result_cost = dls_recursive(adjacente, goal, depth - 1, visited.copy(), path.copy(), vehicle)
                    if result_cost != float('inf'):
                        return result_path, result_cost
            
            return [], float('inf')
        
        # Initialize empty path and visited set
        initial_path = []
        initial_visited = set()
        
        return dls_recursive(start, goal, depth_limit, initial_visited, initial_path, vehicle)

    def IDS(self, start, goal, max_depth, vehicle: Vehicle):
        for depth in range(max_depth):
            path, cost = self.depth_limited_search(start, goal, depth, vehicle)
            if cost != float('inf'):
                return path, cost
        
        return [], float('inf')

    def greedy(self, start, end, vehicle: Vehicle):
        open_list = set([start])
        closed_list = set([])

        parents = {}
        parents[start] = start

        minimum = 0
        distance = 0
        needs = self.get_node_by_name(end).getNeeds()

        for need in needs:
            minimum += need.getSupplyWeightLoad()

        while len(open_list) > 0:
            n = None

            for v in open_list:
                node = self.get_node_by_name(v)
                if n is None or node.getHeuristic() < node.getHeuristic():
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
                area = self.get_node_by_name(end)
                refuel = area.getRefuel()
                vehicle.updateVehicle(distance,needs, True, refuel)
                self.finish_travel(end)
                return (reconst_path, self.calculate_cost(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                if m not in open_list and m not in closed_list and self.compatibleConection(n, m, vehicle) and weight != -1:
                    open_list.add(m)
                    parents[m] = n
                    distance = self.calculate_distance(
                        self.get_node_by_name(start).getLatitude(), self.get_node_by_name(start).getLongitude(),
                        self.get_node_by_name(m).getLatitude(), self.get_node_by_name(m).getLongitude()
                    )
                    time = vehicle.calculateTravelTime(distance)
                    refuel = self.get_node_by_name(m).getRefuel()
                    if vehicle.updateVehicle(distance,needs,False, refuel) is False:
                        break
                    self.update_grafo(time)

            open_list.remove(n)
            closed_list.add(n)

        return [], float('inf')

    def procura_aStar(self, start, end, vehicle: Vehicle):
        open_list = {start} 
        closed_list = set() 

        g = {start: 0}

        parents = {start: None}

        distance = 0
        needs = self.get_node_by_name(end).getNeeds()

        h_start = self.get_node_by_name(start).getHeuristic()

        while open_list:
            n = min(open_list, key=lambda node: g[node] + self.get_node_by_name(node).getHeuristic())

            if n == end:
                path = []
                while n:
                    path.append(n)
                    n = parents[n]
                path.reverse()

                refuel = self.get_node_by_name(end).getRefuel()
                vehicle.updateVehicle(distance, needs, True, refuel)
                self.finish_travel(end)
                return path, self.calculate_cost(path)

            open_list.remove(n)
            closed_list.add(n)

            for m, weight in self.getNeighbours(n):
                if not self.compatibleConection(n, m, vehicle) or weight == -1:
                    continue

                g_new = g[n] + weight

                if m in closed_list and g_new >= g.get(m, float('inf')):
                    continue

                if m not in open_list or g_new < g.get(m, float('inf')):
                    g[m] = g_new
                    parents[m] = n

                    distance = self.calculate_distance(
                        self.get_node_by_name(start).getLatitude(), self.get_node_by_name(start).getLongitude(),
                        self.get_node_by_name(m).getLatitude(), self.get_node_by_name(m).getLongitude()
                    )
                    time = vehicle.calculateTravelTime(distance)
                    refuel = self.get_node_by_name(m).getRefuel()
                    if not vehicle.updateVehicle(distance, needs, False, refuel):
                        continue  

                    self.update_grafo(time)

                    open_list.add(m)

        return [], float('inf')
