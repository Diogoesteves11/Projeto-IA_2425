from Graph.graph import Graph
from Graph.node import Node
from Types.area import Area
from Types.veicule import Vehicle
import time
import tracemalloc
        
def cria_destinos(graph):
    priorityQueue = []
    nodesList = graph.getNodes()
    
    for node in nodesList:
        if node.getAffected(): 
            priorityQueue.append(node)

    priorityQueue.sort(key=lambda node: node.getArea().getPriority(), reverse=True)
    #print(priorityQueue[0])
    return priorityQueue

            
def search(g: Graph, base, vehicles, flag):
    queue = cria_destinos(g)
    destinos_por_veiculo = {v: 0 for v in vehicles}
    caminhos_por_veiculo = {v: [] for v in vehicles}  # Armazena caminhos
    distancia_por_veiculo = {v: 0 for v in vehicles}  # Armazena distâncias
    
    print('------' + base + '-------')
    
    # Iniciar medição de tempo e memória
    start_time = time.time()
    tracemalloc.start()
    current_memory, peak_memory = 0, 0
    
    for i, v in enumerate(vehicles):
        custo_aux = 0
        path_aux = []
        start = base
        v.supplyVehicle(queue)
        #print(f"\nVeículo: {v.getName()}")
        
        while queue:
            end = queue[0]
            goal = end.getName()
            #print(f"Destino atual: {goal}")
            
            # Executar algoritmo selecionado
            if flag == 0:
                path_aux, custo = g.procura_DFS(start, goal, path=[], visited=set(), vehicle=v)
            elif flag == 1:
                path_aux, custo = g.procura_BFS(start, goal, vehicle=v)
            elif flag == 2:
                path_aux, custo = g.procura_custo_uniforme(start, goal, vehicle=v)
            elif flag == 3:
                path_aux, custo = g.IDS(start, goal, 50, vehicle=v)
            elif flag == 4:
                path_aux, custo = g.greedy(start, goal, vehicle=v)
            elif flag == 5:
                path_aux, custo = g.procura_aStar(start, goal, vehicle=v)
            elif flag == 6:
                path_aux, custo = g.simplified_ma_star(start, goal, v, 40)
            
            # Atualizar métricas se encontrou caminho
            if path_aux:
                destinos_por_veiculo[v] += 1
                custo_aux += custo
                caminhos_por_veiculo[v].extend(path_aux)  # Adicionar caminho
                
                # Calcular distância real percorrida
                if len(path_aux) > 1:
                    for i in range(len(path_aux) - 1):
                        node1 = g.get_node_by_name(path_aux[i])
                        node2 = g.get_node_by_name(path_aux[i + 1])
                        dist = g.calculate_distance(
                            node1.getLatitude(), node1.getLongitude(),
                            node2.getLatitude(), node2.getLongitude()
                        )
                        distancia_por_veiculo[v] += dist
                
                start = end.getName()
                queue.pop(0)
            else:
                break
            
            # Atualizar uso de memória
            current, peak = tracemalloc.get_traced_memory()
            current_memory = max(current_memory, current)
            peak_memory = max(peak_memory, peak)
    
    # Calcular tempo total
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Parar rastreamento de memória
    tracemalloc.stop()
    
    # Imprimir relatório detalhado
    print("\n====== Relatório de Execução ======")
    print(f"\nTempo total de execução: {execution_time:.4f} segundos")
    print(f"Uso de memória atual: {current_memory / 10**6:.4f} MB")
    print(f"Pico de memória: {peak_memory / 10**6:.4f} MB")
    
    print("\nResumo por veículo:")
    for v in vehicles:
        print(f"\n{v.getName()}:")
        print(f"- Destinos alcançados: {destinos_por_veiculo[v]}")
        print(f"- Distância total percorrida: {distancia_por_veiculo[v]:.2f} km")
        print(f"- Caminho completo: {' -> '.join(caminhos_por_veiculo[v])}")
    
    # Encontrar veículo com mais destinos
    veiculo_max_destinos = max(destinos_por_veiculo, key=destinos_por_veiculo.get)
    max_destinos = destinos_por_veiculo[veiculo_max_destinos]
    print(f"\nVeículo mais eficiente: {veiculo_max_destinos.getName()} ({max_destinos} destinos)")
    
    time.sleep(30)
    return veiculo_max_destinos, max_destinos
    
    
