

class Veicule:

    def __init__(self, veiculeType: str, maxCapacity: float, autonomy: float ,travelTime: float, averageConsumption: float):
        self.veiculeType: str = veiculeType # veicule type

        self.maxCapacity:float = maxCapacity # max capacity in kg. Static
        self.currentLoad:float = 0 # current capacity occupied

        self.autonomy: float = autonomy # autonomy in Km of the veicule, can be dynamic depending on factor (float: 0 < factor < 1)
        self.distanceCovered: float = 0.0 # distance covered by the veicule in the CURRENT TRAVEL: must be reseted after each travel 
        self.averageConsumption: float = averageConsumption # average Consumption factor in ideal conditions

        self.travelTime: float = travelTime # min/km that the veicule in ideal conditions
        
    
    def getVeiculeType(self) -> str:
        return self.veiculeType
     
    def getMaxCapacity(self) -> float:
        return self.maxCapacity
    
    def getCurrentLoad(self) -> float: 
        return self.currentLoad
    
    def getAutonomy(self, factor: float) -> float:
        return self.autonomy * factor
    
    def getDistanceCovered(self) -> float:
        return self.distanceCovered
    
    def getAverageConsumption(self) -> float:
        return self.averageConsumption

    def getTravelTime(self) -> float:
        return self.travelTime
    
    
    def updateVeicule(self, distanceCovered: float, factor: float) -> bool: # return false if autonomy reaches 0 of if the CurrentLoad exceeds the maxCapacity
        # Calculate load influence (weightLoad)
        weightLoad: float = self.currentLoad / self.maxCapacity
        if weightLoad > 1:
            return False  # Exceeds max capacity
         
        # Calculate fuel consumption
        consumption: float = self.averageConsumption * (1 + weightLoad) * distanceCovered / factor # FACTOR RECEIVED SUPERIOR THEN 1 IS NICE CONDITIONS
        effectiveAutonomy = self.getAutonomy(factor)

        # Check if the vehicle can complete the travel
        if effectiveAutonomy < consumption:
            return False

        # Update vehicle state
        self.autonomy -= consumption
        self.distanceCovered += distanceCovered

        return True

    def calculateTravelTime(self, distance: float ,factor: float) -> float: # returns the time of the travel in minutes. -1 means error. Factor > 1 is nice conditions
        # Calculate load influence (weightLoad)
        weightLoad: float = self.currentLoad / self.maxCapacity
        if weightLoad > 1:
            return -1.0  # Exceeds max capacity
        
        time: float = self.travelTime *  distance * (1 + weightLoad) / factor

        return time

    def newTravel(self, newAutonomy: float):
        self.distanceCovered = 0
        self.currentLoad = 0
        self.autonomy =  newAutonomy # depends on refuel

    