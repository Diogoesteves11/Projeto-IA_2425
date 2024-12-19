from typing import Set
from supply import Supply
from veicule import Veicule

class Travel:
    def __init__(self, veiculeAssigned: Veicule, supplies: set[Supply], factor: float):
        self.veicule: Veicule = veiculeAssigned # veicule assigned to travel
        self.supplies: set[Supply] = supplies # set of supplies to transport. No duplicates
        self.factor: float = factor # initial factor
    

    def getVeiculeAssigned(self) -> Veicule:
        return self.veicule
    
    def getSupplies(self) -> set:
        return self.supplies
    
    def getFactor(self) -> float:
        return self.factor

    def addSupply(self, supply: Supply):
        self.supplies.add(supply)

    def updateFactor(self, factor: int):
        self.factor = factor

    def updateTravel(self, distanceCovered: float) -> bool:
        if not self.veicule.updateVeicule(distanceCovered, self.factor):
            return False
        
        travelTime: float = self.veicule.calculateTravelTime(distanceCovered, self.factor)

        for supply in self.supplies:
            if not supply.updateSupply(travelTime):
                return False
                    
        return True
            

