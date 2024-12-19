import math
from queue import Queue

import networkx as nx  # type: ignore
import matplotlib.pyplot as plt  # type: ignore # idem
from pyvis.network import Network  # type: ignore

from Graph.node import Node
from Types.area import Area

import pandas as pd # type: ignore
import ast

import random

from Types.supply import Supply

from adjustText import adjust_text # type: ignore

class Graph:
    def __init__(self, directed= False):
        self.nodes = []
        self.directed = directed
        self.graph = {}

    def calculate_distance(self,lat1, lon1, lat2, lon2):

        R = 6371  # Radius of Earth in kilometers
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in kilometers

    def add_edge(self, node1, node2):
        n1: Node = self.get_node_by_name(node1)
        n2: Node = self.get_node_by_name(node2)

        if n1 is None:
            print(f"Erro: nó {node1} não encontrado!")
            return  

        if n2 is None:
            print(f"Erro: nó {node2} não encontrado!")
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
            weight = weight = 10000000 # rep do infinito
        else:

            weight = self.calculate_distance(n1.getLatitude(), n1.getLongitude(), n2.getLatitude(), n2.getLongitude())

        self.graph[node1].append((node2, weight))


    def get_node_by_name(self, name):
        search_node = name
        for node in self.nodes:
            if node.getName() == search_node:
                return node
        return None

    def createGraph(self):
        df = pd.read_csv("map.csv")

        for _, row in df.iterrows():
            country = row['Country']
            latitude = row['Latitude']
            longitude = row['Longitude']
            population = row['Population']
            region = row['Region']
            accessibility = row['AccessibilityIndex']

            weather = random.randint(1, 10)
            criticalTime = random.randint(2000, 10080)
            area = Area(country, population, weather, accessibility, region, criticalTime, longitude, latitude)

            supplyTypeNum = random.randint(1, 4)
            supplies = []

            for i in range(supplyTypeNum):
                supply_type = random.choice(["Food", "Water", "Medicine", "Equipment"])
                supply_name = f"{supply_type} {random.randint(1, 100)}"
                supply_weight = random.randint(1, 100)
                supply_quantity = random.randint(1, 100)
                supply_shelf_life = random.choice([random.uniform(0, 10080), float('inf')])

                supply = Supply(supply_type, supply_name, supply_weight, supply_quantity, supply_shelf_life)
                supplies.append(supply)

            node_id = len(self.nodes)
            node = Node(node_id, area, supplies)
            self.nodes.append(node)
            self.graph[country] = []

        for _, row in df.iterrows():
            country = row['Country']
            adjacents = ast.literal_eval(row['Adjacentes'])

            for adjacent in adjacents:
                self.add_edge(country, adjacent)

    def draw(self):
        lista_v = self.nodes
        g = nx.Graph()

        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for adjacente, peso in self.graph[n]:
                if peso == 10000000:
                    peso = -1
                g.add_edge(n, adjacente, weight=round(peso, 2)) 

        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(g, seed=42, k=2, weight='weight') 

        nx.draw_networkx_nodes(g, pos, node_size=300, node_color='lightblue', edgecolors='black')
        nx.draw_networkx_edges(g, pos, edge_color='gray', alpha=0.7, width=1.2)

        nx.draw_networkx_labels(g, pos, font_size=7, font_color='black', font_weight='bold')

        edge_labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=6, label_pos=0.5)

        plt.title("Grafo", fontsize=15)
        plt.axis('off')
        plt.tight_layout()
        plt.show()