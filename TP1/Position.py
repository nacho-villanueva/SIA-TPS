class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        if type(o) is not Position:
            raise TypeError("Expected type Position")
        return Position(self.x + o.x, self.y + o.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
