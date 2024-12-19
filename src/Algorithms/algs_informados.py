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


def getNeighbours(area, nodo):
    lista = []
    for (adjacente, peso) in area.m_graph[nodo]:
        lista.append((adjacente, peso))
    return lista
