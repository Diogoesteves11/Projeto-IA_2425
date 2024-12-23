from Graph.graph import Graph
from Graph.node import Node
from Interface.aidmatrix import App
from Types.veicule import Vehicle
import Algorithms.algs_handler
import time

def main():
    g = Graph()

    supplies_data = g.parse_supplies()
    
    g.createGraph(supplies_data)

    g.draw()
    
    
    vehicles = Vehicle.parse_csv_to_vehicles()
    vehicles_list = list(vehicles.values()) 
    
    time.sleep(10)
    start = g.get_random_node()
    Algorithms.algs_handler.search(g, start, vehicles_list)

    g.draw()
    ##app = App()
    ##app.mainloop()


if __name__ == "__main__":
    main()