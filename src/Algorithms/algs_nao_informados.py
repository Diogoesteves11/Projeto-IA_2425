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

def add_heuristica(area, n, estima):
    n1 = Node(n)
    if n1 in area.m_nodes:
        area.m_h[n] = estima

def procura_aStar(area, start, end):
    open_list = {start}
    closed_list = set([])

    g = {}
    g[start] = 0

    parents = {}
    parents[start] = start

    while len(open_list) > 0:
        n = None

        for v in open_list:
            if n is None or g[v] + area.getH(v) < g[n] + area.getH(n):
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
            return (reconst_path, area.calcula_custo(reconst_path))

        for (m, weight) in area.getNeighbours(n):
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

def getH(area, nodo):
    if nodo not in area.m_h.keys():
        return 1000
    else:
        return area.m_h[nodo]

def greedy(area, start, end):
    open_list = set([start])
    closed_list = set([])

    parents = {}
    parents[start] = start

    while len(open_list) > 0:
        n = None

        for v in open_list:
            if n is None or area.m_h[v] < area.m_h[n]:
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
            return (reconst_path, area.calcula_custo(reconst_path))

        for (m, weight) in area.getNeighbours(n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n

        open_list.remove(n)
        closed_list.add(n)

    print('Path does not exist!')
    return None


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
    
def procura_IDAstar(area, start, end):
    def dfs_f(limit, node, g, path, visited):
        visited.add(node)
        path.append(node)
        
        f = g + area.getH(node)
        if f > limit:
            path.pop()
            visited.remove(node)
            return f 
        
        if node == end:
            return path 
        
        min_limit = float('inf')
        for neighbor, cost in area.getNeighbours(node):
            if neighbor not in visited:
                result = dfs_f(limit, neighbor, g + cost, path, visited)
                if isinstance(result, list):  
                    return result
                min_limit = min(min_limit, result)
        
        path.pop()
        visited.remove(node)
        return min_limit  

    limit = area.getH(start) 
    while True:
        visited = set()
        path = []
        result = dfs_f(limit, start, 0, path, visited)
        if isinstance(result, list):  
            custo = area.calcula_custo(result)
            return (result, custo)
        if result == float('inf'):  
            print("Caminho não encontrado!")
            return None
        limit = result  

