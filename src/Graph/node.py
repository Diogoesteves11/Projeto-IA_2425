from Types.supply import Supply
from Types.area import Area

class Node: 
    def __init__(self, id, area: Area, needs, afected):
        self.id = id
        self.name = str(area.getAreaName())
        self.area = area
        self.needs = needs
        self.afected = afected
    
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
        return self.area.getPriority()
        