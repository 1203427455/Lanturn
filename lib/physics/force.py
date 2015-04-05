from lib.vec2d import Vec2d

class Force(object):
    def __init__(self, vector, source=None):
        self._vector = vector.copy()
        self.source = source

    def update(self, delta):
        return True

    @property
    def vector(self):
        return self._vector.copy()

    @vector.setter
    def vector(self, val):
        raise Exception('Reassigning vector to force is disallowed')

class TimedForce(Force):
    def __init__(self, vector, duration):
        super(TimedForce, self).__init__(vector)
        
        self.elapsed_time = 0
        self.duration = duration

    def update(self, delta):
        self.elapsed_time += delta
        return self.elapsed_time <= self.duration
