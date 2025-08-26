from panda3d.core import NodePath, TextNode


class Bus(NodePath):
    def __init__(self):
        NodePath.__init__(self, "Bus")
        self._distance_traveled = 0
        self._current_coords = None

        # gui
        distance_text = TextNode("distance")
        distance_text.setText(f"Distance traveled: {self._distance_traveled}")
        distance_text.setAlign(TextNode.ALeft)
        self.distance_text_path = aspect2d.attachNewNode(distance_text)
        self.distance_text_path.setScale(0.07)
        self.distance_text_path.setPos(-1.3, 0, 0.9)

    @property
    def distance_traveled(self):
        return self._distance_traveled

    @distance_traveled.setter
    def distance_traveled(self, value):
        self._distance_traveled = value
        self.distance_text_path.node().setText(f"Distance traveled: {self._distance_traveled}")

    @property
    def current_coords(self):
        return self._current_coords

    @current_coords.setter
    def current_coords(self, value):
        self.distance_traveled += self.distance(value)
        self._current_coords = value

    def distance(self, point2):
        """Calculate the Euclidean distance between two points in 2D space."""
        if self._current_coords is None or point2 is None:
            return 0
        return ((self._current_coords.x - point2.x) ** 2 + (self._current_coords.y - point2.y) ** 2) ** 0.5

    def render(self):
        pass
