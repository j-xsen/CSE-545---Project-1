import time
from itertools import permutations

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectSlider import DirectSlider
from panda3d.core import NodePath, CollisionHandlerQueue, CollisionTraverser, CollisionNode, CollisionRay, GeomNode, \
    TextNode

from src.Bus import Bus
from src.City import City


class Map(NodePath):
    def __init__(self, TSP=None):
        NodePath.__init__(self, "map")
        self.reparentTo(render)
        self._TSP = TSP

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

        ## distance slider node
        distance_slider_node = NodePath("DistanceSlider")
        distance_slider_node.setPos(-.95, 0, -.4)
        distance_slider_node.reparentTo(aspect2d)

        # text
        distance_slider_text = TextNode("distance_slider")
        distance_slider_text.setText("Zoom")
        distance_slider_text.setAlign(TextNode.ACenter)
        distance_slider_node_path = distance_slider_node.attachNewNode(distance_slider_text)
        distance_slider_node_path.setScale(0.07)
        distance_slider_node_path.setPos(0, 0, 0.1)

        # slider
        self.slider = DirectSlider(range=(1000, 0), value=500, scale=0.3,
                                   command=lambda: self.setY(self.slider['value']),)
        self.slider.reparentTo(distance_slider_node)


        self.setPos(0, self.slider['value'], 0)
        self.cities = []
        if self.TSP is not None:
            self.create_cities(self.TSP.coords)

    def reset(self):
        for city in self.cities:
            city.selected = False
        self.route = []
        self.route_text.setText("Route: ")
        self.bus.current_coords = None
        self.bus.distance_traveled = 0

    def memory_reset(self):
        self.reset()
        for city in self.cities:
            city.removeNode()
        self.cities = []

    def generate_routes(self):
        results = []
        for p in permutations(range(len(self.cities))):
            self.reset()
            for city_index in p:
                self.select_city(str(city_index + 1))
            results.append((self.bus.distance_traveled, self.route))
        results.sort(key=lambda x: x[0])
        with open(f"results/{self.TSP.name}.txt", "w") as f:
            start_time = time.perf_counter()
            f.write("----- Results -----\n")
            for distance, route in results:
                f.write(f"Distance: {distance}, Route: {', '.join(route)}\n")
            f.write("-------------------")
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            f.write(f"\nExecution time: {execution_time:.6f} seconds\n")
            return

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

    @property
    def TSP(self):
        return self._TSP

    @TSP.setter
    def TSP(self, value):
        self._TSP = value
