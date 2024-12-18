from supply import Supply

class Area: 
    def __init__(self,name: str, needs: {Supply}, density: int, weather: float, region: float, criticalTime: float):
        self.name: str = name
        self.priority: float = (density * 0.8) + (weather * 0.05) + (region * 0.15)
        self.needs:{Supply} = needs
        self.density: int = density
        self.access:float = (weather * 0.5) + (region * 0.4) + (density * 0.1)
        self.criticalTime: float = criticalTime

    def getAreaName(self) -> str:
        return self.name

    def getAreaPriorityIndex(self) -> float:
        return self.priority
    
    def getAreaNeeds(self) -> {Supply}: 
        return self.needs
    
    def getAreaDensity(self) -> int:
        return self.density
    
    def getAreaAccessIndex(self) -> float:
        return self.access

    def getCriticalTime(self) -> float:
        return self.criticalTime
    
    def updateCritivaltime(self, travelTime: float):
        self.criticalTime -= travelTime

