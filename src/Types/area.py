from Types.supply import Supply

class Area: 
    def __init__(self,name: str, density: int, weather: float, access: float, region:str, criticalTime: float, longitude: float, latitude: float):
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.region = str(region)
        self.priority: float = (density * 0.8) + (weather * 0.2)
        self.density: int = density
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
    
    def getAreaDensity(self) -> int:
        return self.density
    
    def getAreaAccessIndex(self) -> float:
        return self.access

    def getCriticalTime(self) -> float:
        return self.criticalTime
    
    def updateCriticaltime(self, travelTime: float):
        self.criticalTime -= travelTime

