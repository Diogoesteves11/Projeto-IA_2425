from Graph.graph import Graph
from Graph.node import Node
from Types.area import Area
import Algorithms.algs_nao_informados 
from Types.veicule import Vehicle

        
def cria_destinos(graph):
    priorityQueue = []
    nodesList = graph.getNodes()
    
    for no in nodesList:
        if(no.afected == True):
            area = Node.getArea(no) 
            priorityQueue.append(area)

    priorityQueue.sort(key=lambda area: Area.getPriority(area), reverse=True)

    return priorityQueue
            
def finish_travel(end):
    end.afected = False
    area = end.getArea()
    area.priority = 0
        
        
#implementar search com funcao de supply veioculo depois da criacao dos destinos

        
    
    