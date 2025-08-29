import sys
from enum import Enum

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, VirtualFileSystem, Filename

from src.Map import Map
from src.TSP import read_tsp

loadPrcFile("./config.prc")

class ProblemType(Enum):
    BRUTE_FORCE = "BF"
    FIRST_SEARCH = "FS"


class TravelingSalesmanProblem(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ShowBase.set_background_color(self, 0, 0, 0.2, 1)

        # load models
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(Filename("models.mf"), ".", VirtualFileSystem.MFReadOnly)

        # disable mouse
        self.disableMouse()

        # accept close program
        self.accept("escape", sys.exit)

        # create buttons to switch between problems
        self.problem_buttons = []
        self.current_problem = None

        # mode
        self.mode = ProblemType.BRUTE_FORCE

        # mode radio buttons
        buttons = [
            DirectRadioButton(text="Brute Force", scale=0.07, pos=(0.9, 0, 0.9), variable=[self.mode], value=[ProblemType.BRUTE_FORCE], command=self.switch_mode, extraArgs=[ProblemType.BRUTE_FORCE]),
            DirectRadioButton(text="Breadth/Depth First Search", scale=0.07, pos=(0.7, 0, 0.8), variable=[self.mode], value=[ProblemType.FIRST_SEARCH], command=self.switch_mode, extraArgs=[ProblemType.FIRST_SEARCH])
        ]
        for button in buttons:
            button.setOthers(buttons)

        # map
        self.map = Map()
        # accept mouse
        self.accept("mouse1-up", self.map.on_mouse_click)

        # default start problem
        self.load_problem(f'Random4.tsp')

    def switch_mode(self, mode):
        if mode == self.mode:
            return
        self.mode = mode
        if mode == ProblemType.BRUTE_FORCE:
            self.load_problem(f'Random4.tsp')
        elif mode == ProblemType.FIRST_SEARCH:
            self.load_problem(f"11PointDFSBFS.tsp")

    def load_problem(self, path):
        if path == self.current_problem:
            return
        self.current_problem = path
        imported_tsp = read_tsp(f"src/tsp/{self.mode.value}/{path}")

        # clear problem buttons
        for button in self.problem_buttons:
            button.destroy()
        self.problem_buttons = []

        self.map.memory_reset()
        self.map.TSP = imported_tsp
        self.map.create_cities(imported_tsp.coords)

        if self.mode == ProblemType.BRUTE_FORCE:
            print("Creating BF buttons")
            # create bruteforce buttons
            for i in range(4, 13):
                extra_arg = f"Random{i}.tsp"
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
