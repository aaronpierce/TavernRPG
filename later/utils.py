from collections import namedtuple

class Coordinate():

    XY = namedtuple('Coordinate', 'x y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return Coordinate.XY(self.x, self.y)

if __name__ == '__main__':

    c = Coordinate(1, 2)

    print(c.get())