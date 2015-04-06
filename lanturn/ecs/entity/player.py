from lib.ecs.system_manager import SystemManager
from lib.ecs.entity.entity import Entity
from lanturn.ecs.message_types import MESSAGE_TYPE
from lanturn.ecs.component.replication import PlayerReplicationComponent
from lanturn.ecs.component.network import NetworkComponent
from lanturn.ecs.entity.pokemon import Pokemon
from lib.vec2d import Vec2d

class Player(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, orientation, username, connection):
        super(Player, self).__init__()
        self.x, self.y = x, y
        self.orientation = orientation
        self.username = username
        self.lineup = [Pokemon(self)]

        self.add_components([
            PlayerReplicationComponent(self),
            NetworkComponent(connection)
        ])

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'player',
            'entity': self
        })

    def move(self, x, y):
        self.x, self.y = x, y

    def get_position(self):
        return (self.x, self.y)