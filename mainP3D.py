from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from TSP import TSP, read_tsp

loadPrcFile("./config.prc")

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ShowBase.set_background_color(self, 0, 0, 0.2, 1)

        # load problem
        self.imported_tsp = read_tsp('Random4.tsp')


app = MyApp()
app.run()
