from Types.supply import Supply

class Area: 
    def __init__(self,name: str, population: int, weather: int, access: float, region:str, criticalTime: float, longitude: float, latitude: float):
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.region = str(region)
        self.population: int = population
        self.access:float = access
        self.weather = weather
        self.priority: float = ((10000/criticalTime) * 0.4) + ((population / 10**6) * 0.6 )
        

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

    def getWeather(self) -> int:
        return self.weather
    
    
    def getCriticalTime(self) -> float:
        return self.criticalTime
    
    def updateCriticaltime(self, travelTime: float):
        self.criticalTime -= travelTime
        
    def updatePriority(self):
        self.priority = ((10000/self.criticalTime) * 0.4) + ((self.population/10**6) * 0.6)

    def getPriority(self):
        return self.priority

