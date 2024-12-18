import math
from queue import Queue

import networkx as nx  # type: ignore # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # type: ignore # idem

import node
from Types.area import Area

class Graph:
    def __init__(self, directed= False):
        self.nodes = []
        self.directed = directed
        self.graph = {}
    
    def add_edge(self, node1, node2, weight):
        n1 = Area(node1)
        n2 = Area(node2)
        if (n1 not in self.nodes):
            n1_id = len(self.nodes)  
            n1.setId(n1_id)
            self.nodes.append(n1)
            self.graph[node1] = []
        

        if (n2 not in self.nodes):
            n2_id = len(self.nodes)  
            n2.setId(n2_id)
            self.nodes.append(n2)
            self.graph[node2] = []
        

        self.graph[node1].append((node2, weight))  