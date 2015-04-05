class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if width < 0:
            raise ValueError('Width has a negative value!')

        if height < 0:
            raise ValueError('Height has a negative value!')

    def get_min_max(self):
        min_x = self.x
        max_x = self.x + self.width - 1
        min_y = self.y
        max_y = self.y + self.height - 1

        return min_x, max_x, min_y, max_y

    def intersects(self, other):
        self_min_x, self_max_x, self_min_y, self_max_y = self.get_min_max()
        other_min_x, other_max_x, other_min_y, other_max_y = other.get_min_max()

        return not (any([self_min_x > other_max_x, self_max_x < other_min_x,
            self_min_y > other_max_y, self_max_y < other_min_y]))
