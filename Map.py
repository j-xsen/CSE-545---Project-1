from itertools import permutations

from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath, CollisionHandlerQueue, CollisionTraverser, CollisionNode, CollisionRay, GeomNode, \
    TextNode

from Bus import Bus
from City import City


class Map(NodePath):
    def __init__(self, TSP=None):
        NodePath.__init__(self, "map")
        self.reparentTo(render)
        self.TSP = TSP

        # add collision traverser and handler
        self.c_trav = CollisionTraverser()
        self.c_handler = CollisionHandlerQueue()

        self.route_text = TextNode("route")
        self.route_text.setText("Route: ")
        self.route_text.setAlign(TextNode.ALeft)
        self.route_text_path = aspect2d.attachNewNode(self.route_text)
        self.route_text_path.setScale(0.07)
        self.route_text_path.setPos(-1.3, 0, 0.8)
        self.route = []

        self.bus = Bus()

        self.generate_routes_button = DirectButton(text="Generate Routes", scale=0.07,
                                                    pos=(1, 0, -0.9),
                                                   command=self.generate_routes)
        self.reset_button = DirectButton(text="Reset", scale=0.07,
                                         pos=(1, 0, -0.8),
                                         command=self.reset)

        self.setPos(0, 500, 0)
        self.cities = []

    def reset(self):
        for city in self.cities:
            city.selected = False
        self.route = []
        self.route_text.setText("Route: ")
        self.bus.current_coords = None
        self.bus.distance_traveled = 0

    def generate_routes(self):
        results = []
        for p in permutations(range(len(self.cities))):
            self.reset()
            for city_index in p:
                self.select_city(str(city_index + 1))
            results.append((self.bus.distance_traveled, self.route))
        results.sort(key=lambda x: x[0])
        with open(f"{self.TSP.name}.txt", "w") as f:
            f.write("----- Results -----\n")
            for distance, route in results:
                f.write(f"Distance: {distance}, Route: {', '.join(route)}\n")
            f.write("-------------------")

    def create_city(self, name, coords):
        new_city = City(name, coords)
        new_city.reparentTo(self)
        self.cities.append(new_city)

    def create_cities(self, coords_list):
        city_id = 1
        for coords in coords_list:
            self.create_city(city_id, coords)
            city_id += 1

    def select_city(self, city_id):
        if self.cities[int(city_id) - 1].selected:
            print(f"City {city_id} already selected")
            return
        self.route.append(city_id)
        self.route_text.setText(f"Route: {', '.join(self.route)}")
        self.bus.current_coords = self.cities[int(city_id) - 1].coords
        self.cities[int(city_id) - 1].selected = True

    def on_mouse_click(self):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            pickerNode = CollisionNode('mouseRay')
            pickerNP = base.camera.attachNewNode(pickerNode)
            pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
            pickerRay = CollisionRay()
            pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            pickerNode.addSolid(pickerRay)
            self.c_trav.addCollider(pickerNP, self.c_handler)
            self.c_trav.traverse(base.render)
            if self.c_handler.getNumEntries() > 0:
                self.c_handler.sortEntries()
                pickedObj = self.c_handler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag("ClickableCity")
                if not pickedObj.isEmpty():
                    self.select_city(str(pickedObj).split("-")[1])
            pickerNP.removeNode()
