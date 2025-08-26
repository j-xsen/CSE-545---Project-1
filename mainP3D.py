import sys

from panda3d.core import loadPrcFile, NodePath, TextNode, CollisionTraverser, CollisionHandlerQueue, CollisionRay, \
    CollisionNode, GeomNode
from direct.showbase.ShowBase import ShowBase
from TSP import TSP, read_tsp

loadPrcFile("./config.prc")

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ShowBase.set_background_color(self, 0, 0, 0.2, 1)

        # add collision traverser and handler
        self.c_trav = CollisionTraverser()
        self.c_handler = CollisionHandlerQueue()

        # disable mouse
        self.disableMouse()

        # accept close program
        self.accept("escape", sys.exit)
        # accept mouse
        self.accept("mouse1-up", self.on_mouse_click)

        # load problem
        self.imported_tsp = read_tsp('Random4.tsp')

        # map
        self.map = NodePath("map")
        self.map.reparentTo(self.render)
        self.map.setPos(0,500,0)

        # create cities
        for city_coords in self.imported_tsp.coords:
            print("Creating city at:", city_coords)
            city = self.create_city(city_coords)
            city.reparentTo(self.map)

    def create_city(self, coord):
        new_city = City(self.map, coord)
        return new_city

    def on_mouse_click(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            print("Mouse clicked at:", mpos)
            pickerNode = CollisionNode('mouseRay')
            pickerNP = self.camera.attachNewNode(pickerNode)
            pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
            pickerRay = CollisionRay()
            pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            pickerNode.addSolid(pickerRay)
            self.c_trav.addCollider(pickerNP, self.c_handler)
            self.c_trav.traverse(self.render)
            if self.c_handler.getNumEntries() > 0:
                self.c_handler.sortEntries()
                pickedObj = self.c_handler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag("ClickableCity")
                if not pickedObj.isEmpty():
                    print("Picked object:", pickedObj)
            pickerNP.removeNode()

class City(NodePath):
    def __init__(self, parent, coord):
        NodePath.__init__(self, f"city-{coord.x}-{coord.y}")
        self.setTag("ClickableCity", "1")
        self.coord = coord
        self.model = loader.loadModel("bam/square.bam")
        self.model.reparentTo(self)
        self.model.setScale(2,2,2)
        self.model.setPos(coord.x-50, 0, coord.y-50)

        self.title_node = TextNode("title")
        self.title_node.setText(f"{coord.name}")
        self.title_node.setAlign(TextNode.ACenter)
        self.title_node_path = self.model.attachNewNode(self.title_node)
        self.title_node_path.setScale(5)
        self.title_node_path.setPos(0,0,2)
        self.title_node_path.setBillboardPointEye()

    def render(self):
        pass

app = MyApp()
app.run()
