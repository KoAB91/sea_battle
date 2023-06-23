class Dot:

    x = None
    y = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False
