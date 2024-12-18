from Types.supply import Supply
from Types.area import Area

class Node: 
    def __init__(self, name: str, needs: {Supply}, density: int, weather: float, region: float, criticalTime: float, id = -1):
        self.id = id
        self.name = str(name)
        self.area = Area(name, needs, density, weather, region, criticalTime)

    