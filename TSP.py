class Coord:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return f"Coord {self.name}: ({self.x}, {self.y})"


class TSP:
    def __init__(self, name="", dimension=0, coords=None):
        if coords is None:
            coords = []
        self._name = name
        self.dimension = dimension
        self.coords = coords

    def add_coord(self, name, x, y):
        self._coords.append(Coord(name, x, y))

    @property
    def name(self): # getter
        return self._name
    @name.setter
    def name(self, value): # setter
        self._name = value

    @property
    def dimension(self):
        return self._dimension
    @dimension.setter
    def dimension(self, value):
        self._dimension = value

    @property
    def coords(self):
        return self._coords
    @coords.setter
    def coords(self, value):
        self._coords = value

    def __str__(self):
        print("--- TSP Instance ---")
        print(f"Name: {self.name}")
        print(f"Dimension: {self.dimension}")
        for coord in self._coords:
            print(coord)
        return "--------------------"


scale = 1
def read_tsp(path):
    print("Creating TSP")
    new_tsp = TSP()
    with open(path, 'r', encoding="utf-8") as f:
        coord_section = False
        for line in f:
            if not coord_section:
                split = line.strip().split(":")
                if split[0] == "NAME":
                    new_tsp.name = split[1].strip()
                elif split[0] == "DIMENSION":
                    new_tsp.dimension = int(split[1].strip())
                elif split[0] == "NODE_COORD_SECTION":
                    coord_section = True
            else:
                if line.strip() == "EOF":
                    break
                split = line.strip().split()
                name = int(split[0])
                x_cord = float(split[1])*scale
                y_cord = float(split[2])*scale
                new_tsp.add_coord(name, x_cord, y_cord)
    print(new_tsp)
    return new_tsp
