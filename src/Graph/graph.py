import math
from queue import Queue

import networkx as nx  # type: ignore # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # type: ignore # idem

import node

class Graph:
    def __init__(self, directed= False):
        self.nodes = []
        self.directed = directed
        self.graph = {}
    