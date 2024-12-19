from Types.supply import Supply

class Area: 
    def __init__(self,name: str, population: int, weather: float, access: float, region:str, criticalTime: float, longitude: float, latitude: float):
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.region = str(region)
        self.density: int = population
        self.access:float = access

        critical_impact = 1 / criticalTime if criticalTime > 0 else 0  
        self.priority: float = (
            (criticalTime * 0.5) +      # Peso de 50% para criticalTime
            ((population / 10**6) * 0.2) +  # Peso de 20% para população
            (weather * 0.2) +           # Peso de 20% para clima
            (access * 0.1)              # Peso de 10% para acesso
        )

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

    def getPriority(self):
        return self.priority

