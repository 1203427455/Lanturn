import json
from lib.ecs.system_manager import SystemManager
from lanturn.ecs.entity.player import Player
from lanturn.ecs.system.replication import ReplicationSystem
from lanturn.ecs.system.battle import BattleSystem
from lanturn.ecs.message_types import MESSAGE_TYPE
from lanturn.ecs.entity.pokemon import Pokemon

class Game(object):
    LEVEL_DIMENSION = 10
    
    def __init__(self):
        self.users = {}
        self.username_to_id = {}
        self.zone = [[None for i in range(self.LEVEL_DIMENSION)] for j in range(self.LEVEL_DIMENSION)]
        self.system_manager = SystemManager.get_instance()
        self.system_manager.init([
            ReplicationSystem(),
            BattleSystem()
        ])

    def get_message_handlers(self):
        return {
            'connect': self.connect,
            'move': self.move,
        }

    def get_free_position(self):
        for i in range(self.LEVEL_DIMENSION):
            for j in range(self.LEVEL_DIMENSION):
                if self.zone[i][j] is None:
                    return i, j

        return None

    def register_new_user(self, username, connection):
        x, y = self.get_free_position()
        player = Player(x, y, 0, username, connection)
        self.username_to_id[username] = player.id
        self.users[player.id] = player
        self.zone[x][y] = True

        return player.id

    def connect(self, message):
        data = message.data
        username = data['username']
        connection = message.connection

        if username not in self.username_to_id:
            player_id = self.register_new_user(username, connection)
        else:
            player_id = self.username_to_id[username]

        self.users[player_id].connection = connection
        connection.player_id = player_id

        connection.sendMessage(json.dumps({
            'type': 'connect_response',
            'player_id': player_id
        }))

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CLIENT_CONNECT,
            'connection': connection,
        })

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_BATTLE,
            'team_a_settings': {'lineups': [self.users[player_id].lineup], 'size': 1},
            'team_b_settings': {'lineups': [[Pokemon(None)]], 'size': 1},
            'players': [self.users[player_id]]
        })

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.PLAYER_BATTLE_MOVE,
            'pokemon': self.users[player_id].lineup[0],
            'player': self.users[player_id]
        })

        return player_id

    def move(self, message):
        data = message.data
        player_id = message.player_id

        new_x, new_y = data['position']
        old_x, old_y = self.users[player_id].x, self.users[player_id].y
        orientation = data['orientation']
        self.users[player_id].orientation = orientation

        if new_x >= self.LEVEL_DIMENSION or new_y >= self.LEVEL_DIMENSION or self.zone[new_x][new_y]:
            # Position is already occupied or is invalid
            message.connection.sendMessage(json.dumps({
                'type': 'invalid_move',
            }))
        else:
            self.zone[old_x][old_y] = None
            self.zone[new_x][new_y] = True
            self.users[player_id].move(new_x, new_y)

    def update(self, delta):
        self.system_manager.update(delta)
