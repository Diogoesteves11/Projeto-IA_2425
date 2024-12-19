
class Supply:

    def __init__(self, type: str, name: str, weight: int, quantity: int ,shelfLife: float):
        self.type: str = type # supply type
        self.name: str = name # supply name
        self.weight: float = weight # supply weight in Kg
        self.quantity: int = quantity # number of supplies available 
        self.shelfLife: float = shelfLife # supply shelf life. if its zero means the supply is no longer usable. Can be infinite (minutes) 
    
    def getSupplyType(self) -> str:
        return self.type
    
    def getSupplyName(self) -> str:
        return self.name
    
    def getSupplyWeightLoad(self) -> int:
        return self.weight * self.quantity
    
    def getSupplyShelfLife(self) -> float:
        return self.shelfLife

    def updateSupply(self, travelTime: float) -> bool:
        self.shelfLife -= travelTime
        if self.shelfLife < 0: return False

        return True