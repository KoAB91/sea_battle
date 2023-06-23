from Dot import Dot


class Ship:
    dots = None
    length = None
    head = None
    direction = None
    lives = None

    def __init__(self, length: int, head: Dot, direction: int):
        self.dots = []
        self.length = length
        self.head = head
        self.direction = direction
        self.lives = length
        self.dots.append(head)
        if length > 1:
            head_x = head.get_x()
            head_y = head.get_y()
            if direction:
                for i in range(1, length):
                    self.dots.append(Dot(head_x, head_y + i))
            else:
                for i in range(1, length):
                    self.dots.append(Dot(head_x + i, head_y))

    def get_dots(self):
        return self.dots

    def get_length(self):
        return self.length

    def get_head(self):
        return self.head

    def get_direction(self):
        return self.direction

    def get_lives(self):
        return self.lives

    def set_lives(self, values):
        self.lives = values
