from panda3d.core import NodePath, TextNode, Material


class City(NodePath):
    def __init__(self, name, coord):
        NodePath.__init__(self, f"city-{name}")
        self.setTag("ClickableCity", str(name))
        self.coords = coord
        self.model = loader.loadModel("bam/square.bam")
        self.model.setColor((0,1,0,1))
        self.model.reparentTo(self)
        self.model.setScale(2,2,2)
        self.model.setPos(coord.x-50, 0, coord.y-50)

        self._name = name

        self.title_node = TextNode("title")
        self.title_node.setText(f"{name}")
        self.title_node.setAlign(TextNode.ACenter)
        self.title_node_path = self.model.attachNewNode(self.title_node)
        self.title_node_path.setScale(5)
        self.title_node_path.setPos(0,0,2)
        self.title_node_path.setBillboardPointEye()

        self.selected = False

    @property
    def selected(self):
        return self._selected
    @selected.setter
    def selected(self, value):
        try:
            if self._selected == value:
                return
        except AttributeError:
            pass
        self._selected = value
        if self._selected:
            self.model.setColor((1,0,0,1))
        else:
            self.model.setColor((0,1,0,1))

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    def render(self):
        pass
