from Graph.graph import Graph
from Graph.node import Node
from Types.area import Area
from Types.veicule import Vehicle

        
def cria_destinos(graph):
    priorityQueue = []
    nodesList = graph.getNodes()
    
    for node in nodesList:
        if node.getAffected(): 
            priorityQueue.append(node)

    priorityQueue.sort(key=lambda node: node.getArea().getPriority(), reverse=True)
    #print(priorityQueue[0])
    return priorityQueue

            
def search(g: Graph, base, vehicles):
    queue = cria_destinos(g)
    
    destinos_por_veiculo = {v: 0 for v in vehicles}
    print('------' + base + '-------')
    for i, v in enumerate(vehicles):
        custo_aux = 0
        path_aux = []
        start = base

        
        v.supplyVehicle(queue)
        print(v.getName() + '--------')
        
        while queue:
            end = queue[0]
            goal = end.getName()
            print(goal)
            #path_aux, custo = g.procura_DFS(start, goal, path=[], visited=set(), vehicle=v)
            #path_aux, custo = g.procura_BFS(start, goal, vehicle=v)
            #path_aux, custo = g.procura_custo_uniforme(start, goal, vehicle=v)
            #path_aux, custo = g.greedy(start, goal, vehicle=v)
            path_aux, custo = g.procura_aStar(start, goal, vehicle=v)
            print(path_aux)
            if path_aux:
                destinos_por_veiculo[v] += 1
                custo_aux += custo
                start = end.getName()  # Atualiza o próximo início
                end = queue.pop(0)
            else:
                break
            

    veiculo_max_destinos = max(destinos_por_veiculo, key=destinos_por_veiculo.get)
    max_destinos = destinos_por_veiculo[veiculo_max_destinos]
    
    print(f"Veículo que percorreu mais destinos: {veiculo_max_destinos.getName()} ({max_destinos} destinos)->  " + str(path_aux))
    return veiculo_max_destinos, max_destinos

    
    
