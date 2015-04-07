from lib.ecs.system.system import System
from lanturn.ecs.message_types import MESSAGE_TYPE
from lanturn.battle.battle import Battle, BattleAI

class BattleSystem(System):
    def __init__(self):
        message_handlers = {
            MESSAGE_TYPE.CREATE_BATTLE: self.handle_create_battle,
            MESSAGE_TYPE.PLAYER_BATTLE_MOVE: self.handle_player_battle_move,
        }
        self.player_to_battle = {}

        super(BattleSystem, self).__init__(message_handlers)

    def handle_player_battle_move(self, message):
        player = message['player']
        pokemon = message['pokemon']
        battle = self.player_to_battle[player]
        battle.accept_move(player, BattleAI().generate_move(pokemon))

    def handle_create_battle(self, message):
        players = message['players']
        battle = Battle(message['team_a_settings'], message['team_b_settings'], players)
        for player in players:
            self.player_to_battle[player] = battle

    def update(self, delta):
        self.handle_messages()
