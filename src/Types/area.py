from Types.supply import Supply

class Area: 
    def __init__(self,name: str, population: int, weather: float, access: float, region:str, criticalTime: float, longitude: float, latitude: float):
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.region = str(region)
        self.priority: float = (population * 0.4) + (weather * 0.6)
        self.density: int = population
        self.access:float = access
        self.criticalTime: float = criticalTime

    def getAreaName(self) -> str:
        return self.name
    
    def getLongitude(self) -> float:
        return self.longitude
    
    def getLatitude(self) -> float:
        return self.latitude

    def getAreaPriorityIndex(self) -> float:
        return self.priority
    
    def getAreaPopulation(self) -> int:
        return self.density
    
    def getAreaAccessIndex(self) -> float:
        return self.access

    def getCriticalTime(self) -> float:
        return self.criticalTime
    
    def updateCriticaltime(self, travelTime: float):
        self.criticalTime -= travelTime

