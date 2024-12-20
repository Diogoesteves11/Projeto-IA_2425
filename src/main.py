from Graph.graph import Graph
from Interface.aidmatrix import App



def main():
    g = Graph()

    supplies_data = g.parse_supplies()
    
    g.createGraph(supplies_data)

    g.draw()

    app = App()

    app.mainloop()


if __name__ == "__main__":
    main()