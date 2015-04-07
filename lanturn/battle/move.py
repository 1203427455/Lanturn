import random

class Move(object):
    def __init__(self, source, target, move_type=1, damage=None):
        self.source = source
        self.target = target
        self.type = move_type
        self.damage = random.randint(1, 100) if damage is None else damage

    def execute(self):
        self.target.health -= self.damage
