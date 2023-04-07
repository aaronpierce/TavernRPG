class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield from [self.x, self.y]

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)