

class veicule:

    def __init__(self, veiculeType: str, maxCapacity: int, autonomy: float, travelTime: float):
        self.veiculeType = veiculeType # veicule type
        self.maxCapacity = maxCapacity # max capacity in kg. Static
        self.autonomy = autonomy # autonomy in Km of the veicule, can be dynamic depending on factor (float: 0 < factor < 1)
        self.travelTime = travelTime # min/km that the veicule. Can be dynamic depending on factor (float: 0 < factor < 1)
        self.distanceCovered: float = 0.0 # distance covered by the veicule in the CURRENT TRAVEL: must be reseted after each travel 
    
    def getVeiculeType(self) -> str:
        return self.veiculeType
    
    def getMaxCapacity(self) -> float:
        return self.maxCapacity
    
    def getAutonomy(self, factor: float) -> float:
        return self.autonomy * factor

    def getTravelTime(self, factor: float) -> float:
        return self.travelTime * factor
    
    
    
    def resetDistance(self):
        self.distanceCovered = 0
    