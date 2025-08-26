import sys

from direct.gui.DirectButton import DirectButton
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, CollisionRay, \
    CollisionNode, GeomNode

from Map import Map
from TSP import read_tsp

loadPrcFile("./config.prc")


class TravelingSalesmanProblem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ShowBase.set_background_color(self, 0, 0, 0.2, 1)

        # disable mouse
        self.disableMouse()

        # accept close program
        self.accept("escape", sys.exit)

        # load problem
        self.imported_tsp = read_tsp('tsp/Random4.tsp')

        # create buttons to switch between problems
        self.problem_buttons = []
        self.current_problem = None

        # map
        self.map = Map(TSP=self.imported_tsp)
        # accept mouse
        self.accept("mouse1-up", self.map.on_mouse_click)

        self.load_problem('tsp/Random4.tsp')

    def load_problem(self, path):
        if path == self.current_problem:
            return
        self.current_problem = path
        self.imported_tsp = read_tsp(path)
        self.problem_buttons.clear()

        self.map.memory_reset()
        self.map.create_cities(self.imported_tsp.coords)

        for i in range(4, 13):
            extra_arg = f"tsp/Random{i}.tsp"
            col = (i - 4) % 3
            row = (i - 4) // 3

            button = DirectButton(
                text=f"Random{i}",
                scale=0.07,
                frameColor=((0.8, 0.8, 0.8, 1) if extra_arg != self.current_problem else (0.2, 0.2, 0.2, 1)),
                pos=(-1.1 + col * 0.4, 0, -row * 0.15 - 0.6),
                command=self.load_problem,
                extraArgs=[extra_arg]
            )

            self.problem_buttons.append(button)


app = TravelingSalesmanProblem()
app.run()
