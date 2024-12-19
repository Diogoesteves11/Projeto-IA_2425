from Graph.graph import Graph
from Interface.aidmatrix import App


def main():
    g = Graph()

    g.createGraph()

    g.draw()

    app = App()

    app.mainloop()


if name == "main":
    main()