import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, CollisionRay, \
    CollisionNode, GeomNode

from Map import Map
from TSP import read_tsp

loadPrcFile("./config.prc")


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ShowBase.set_background_color(self, 0, 0, 0.2, 1)

        # disable mouse
        self.disableMouse()

        # accept close program
        self.accept("escape", sys.exit)

        # load problem
        self.imported_tsp = read_tsp('tsp/Random12.tsp')

        # map
        self.map = Map(TSP=self.imported_tsp)
        # accept mouse
        self.accept("mouse1-up", self.map.on_mouse_click)

        # create cities
        self.map.create_cities(self.imported_tsp.coords)


app = MyApp()
app.run()
