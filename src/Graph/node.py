from Types.supply import Supply
from Types.area import Area
from Types.veicule import Vehicle

class Node: 
    def __init__(self, id, area: Area, needs, afected, refuel):
        self.id = id
        self.name = str(area.getAreaName())
        self.area = area
        self.needs = needs
        self.afected = afected
        self.refuel = refuel

    def getRefuel(self):
        return self.refuel

    def setAffected(self, affected):
        self.afected = affected

    def getAffected(self):
        return self.afected
    
    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id
    
    def getArea(self):
        return self.area
    
    def getNeeds(self):
        return self.needs

    def getName(self):
        return self.name
    
    def getLatitude(self):
        return self.area.getLatitude()
    
    def getLongitude(self):
        return self.area.getLongitude()
    
    def getAfected(self):
        return self.afected

    def getHeuristic(self):
        return self.area.getPriority() + self.area.getAreaAccessIndex() + self.area.getWeather()
        
    def updateCriticalTime(self, traveltime):
        self.area.updateCriticaltime(traveltime)
    
    def updatePriority(self):
        self.area.updatePriority()

    def supplyArea(self, vehicle: Vehicle, minimumWeight, distance, mainAreaName):
        loadAfterSupply = 0
        needLoad = 0
        vehicleLoad = vehicle.getCurrentLoad()
        for need in self.needs:
            needLoad += need.getSupplyWeightLoad()
        
        loadAfterSupply = vehicleLoad - needLoad

        if self.name == mainAreaName: 
            vehicle.updateVehicle(distance, self.needs, True)
            self.needs = []
            self.afected = False
            return False          

        if loadAfterSupply > 0 and loadAfterSupply > minimumWeight:
            vehicle.updateVehicle(distance, self.needs, True)
            self.needs = []
            self.afected = False
            return True 
        
        if loadAfterSupply < 0 or loadAfterSupply <= minimumWeight:
            return True 

        return False
        
        
        