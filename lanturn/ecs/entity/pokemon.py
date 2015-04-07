from lib.ecs.system_manager import SystemManager
from lib.ecs.entity.entity import Entity

class Pokemon(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, owner):
        super(Pokemon, self).__init__()
        self.type = 0
        self.health = 100
        self.owner = owner

    def __str__(self):
    	return '<Pokemon {}>'.format(self.id)