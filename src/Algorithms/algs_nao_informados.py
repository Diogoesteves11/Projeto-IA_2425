from queue import Queue
import heapq

def procura_DFS(area, start, end, path=[], visited=set()):
    path.append(start)
    visited.add(start)

    if start == end:
        custoT = area.calcula_custo(path)
        return (path, custoT)
    
    for (adjacente, peso) in area.m_graph[start]:
        if adjacente not in visited:
            resultado = area.procura_DFS(adjacente, end, path, visited)
            if resultado is not None:
                return resultado
    
    path.pop()
    return None

def procura_BFS(area, start, end, direction):
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
            neighbors = area.m_graph[nodo_atual] 
        elif direction == 'backward':
            neighbors = [(adjacente, peso) for adjacente, peso in area.getNeighbours(nodo_atual) 
                         if nodo_atual in [adj[0] for adj in area.m_graph[adjacente]]]

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
        custo = area.calcula_custo(path)
    return (path, custo)


def getNeighbours(area, nodo):
    lista = []
    for (adjacente, peso) in area.m_graph[nodo]:
        lista.append((adjacente, peso))
    return lista

def is_intersecting(area):
    
    for i in range(area.vertices):
        if(area.start_visited[i] and area.dest_visited[i]):
            return i
    
    return -1

def procura_BiDir(area, start, end):
    area.start_queue.append(start)
    area.start_visited[start] = True
    area.start_parent[start] = -1
    
    area.end_queue.append(end)
    area.end_visited[end] = True
    area.end_parent[end] = -1
    
    while area.start_queue and area.end_queue:
        procura_BFS(area, start, end, direction = 'forward')
        
        procura_BFS(area, start, end, direction = 'backward')
        
        intersecting_node = is_intersecting(area)
        
        if intersecting_node != -1:
            print(f"Caminho entre {start} e {end} existe")
            print(f"Interseção em: {intersecting_node}")
            
            exit(0)
        
    return -1
   
def reconstruct_path(visited, start, end):
    path = []
    current = end 
    while current is not None:
        path.append(current) 
        current = visited[current][1]
        
    path.reverse()
    return path
        
def procura_custo_uniforme(area, start, end):
    priority_queue = [(0, start)]
    visited = {start: (0, None)}
    
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            return current_cost, reconstruct_path(visited, start, goal)
        
        for neighbor, cost in area[current_node]:
            total_cost = current_cost + cost
            
            if neighbor not in visited or total_cost < visited[neighbor][0]:
                visited[neighbor] = (total_cost, current_node)
                heapq.heappush(priority_queue, (total_cost, neighbor))
    
    return None
    
