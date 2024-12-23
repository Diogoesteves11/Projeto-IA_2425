import csv
from Graph.node import *

class Vehicle:
    def __init__(self, vehicleName: str, vehicleType: str, maxCapacity: float, autonomy: float, travelTime: float, averageConsumption: float):
        self.vehicleName: str = vehicleName
        self.vehicleType: str = vehicleType  # Vehicle type

        self.maxCapacity: float = maxCapacity  # Max capacity in kg
        self.currentLoad: float = 0  # Current capacity occupied

        self.autonomy: float = autonomy  # Autonomy in Km
        self.initialAutonomy = autonomy
        self.distanceCovered: float = 0.0  # Distance covered in the current travel
        self.averageConsumption: float = averageConsumption  # Average consumption in ideal conditions

        self.travelTime: float = travelTime  # Time per km in ideal conditions


    def getName(self):
        return self.vehicleName
    
    @staticmethod
    def parse_csv_to_vehicles():
        vehicles = {}

        with open("vehicles.csv", 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                vehicles[name] = Vehicle(
                    vehicleName=name,
                    vehicleType=row['Type'],
                    maxCapacity=float(row['MaxCapacity']),
                    autonomy=float(row['Autonomy']),
                    travelTime=float(row['TravelTime']),
                    averageConsumption=float(row['AverageConsumption'])
                )

        return vehicles

    def getvehicleName(self) -> str:
        return self.vehicleName

    def getvehicleType(self) -> str:
        return self.vehicleType
     
    def getMaxCapacity(self) -> float:
        return self.maxCapacity
    
    def getCurrentLoad(self) -> float: 
        return self.currentLoad
    
    def getAutonomy(self) -> float:
        return self.autonomy 
    
    def getDistanceCovered(self) -> float:
        return self.distanceCovered
    
    def getAverageConsumption(self) -> float:
        return self.averageConsumption

    def getTravelTime(self) -> float:
        return self.travelTime
    
    
    def updateVehicle(self, distanceCovered: float, needs, forSupply: bool, refuel) -> bool: # return false if autonomy reaches 0 of if the CurrentLoad exceeds the maxCapacity
        # Calculate load influence (weightLoad)
        weightLoad: float = self.currentLoad / self.maxCapacity
        if weightLoad > 1:
            return False  # Exceeds max capacity
         
        # Calculate fuel consumption
        consumption: float = self.averageConsumption * (1 + weightLoad) * distanceCovered  # FACTOR RECEIVED SUPERIOR THEN 1 IS NICE CONDITIONS
        effectiveAutonomy = self.getAutonomy()

        if refuel is True: 
            self.autonomy = self.initialAutonomy

        # Check if the vehicle can complete the travel
        if effectiveAutonomy < consumption:
            return False

        # Update vehicle state
        self.autonomy -= consumption
        self.distanceCovered += distanceCovered

        if forSupply:
            for supply in needs:
                supplyWeight = supply.getSupplyWeightLoad()
                if self.currentLoad >= supplyWeight:
                    self.currentLoad -= supplyWeight
                else: 
                    self.currentLoad = 0

        return True

    def calculateTravelTime(self, distance: float) -> float: # returns the time of the travel in minutes. -1 means error. Factor > 1 is nice conditions
        # Calculate load influence (weightLoad)
        weightLoad: float = self.currentLoad / self.maxCapacity
        if weightLoad > 1:
            return -1.0  # Exceeds max capacity
        
        time: float = self.travelTime *  distance * (1 + weightLoad)

        return time

    def newTravel(self, newAutonomy: float):
        self.distanceCovered = 0
        self.currentLoad = 0
        self.autonomy =  newAutonomy # depends on refuel

    
    def supplyVehicle(self, queue):
        for node in queue:
            needs = node.getNeeds()

            for supply in needs:
                available_space = self.maxCapacity - self.currentLoad
                if available_space <= 0:
                    break 

                loadable_quantity = min(supply.quantity, available_space // supply.weight)

                if loadable_quantity > 0:
                    self.currentLoad += loadable_quantity * supply.weight
        