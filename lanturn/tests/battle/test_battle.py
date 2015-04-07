import unittest

from lanturn.ecs.entity.player import Player
from lanturn.ecs.entity.pokemon import Pokemon
from lanturn.ecs.system.battle import Battle
from lib.ecs.system_manager import SystemManager
from lanturn.ecs.system.battle import BattleSystem
from lanturn.arena import Move

class TestOne(unittest.TestCase):
    def test_one_vs_one(self):
        SystemManager.get_instance().init([
            BattleSystem()
        ])

        player_one = Player(0, 0, 0, 'player one', None)
        player_two = Player(0, 0, 0, 'player two', None)

        p1 = Pokemon(player_one)
        p2 = Pokemon(player_two)

        p3 = Pokemon(player_one)
        p4 = Pokemon(player_two)

        team_a_settings = {
            'lineups': [[p1, p3]],
            'size': 1
        }

        team_b_settings = {
            'lineups': [[p2, p4]],
            'size': 1
        }

        battle = Battle(team_a_settings, team_b_settings, [player_one, player_two])
        battle.accept_move(player_one, Move(p1, p2, damage=50))
        battle.accept_move(player_two, Move(p2, p1, damage=50))
        battle.accept_move(player_one, Move(p1, p2, damage=50))
        battle.accept_move(player_two, Move(p2, p1, damage=50))
        battle.accept_move(player_two, Move(p4, None, move_type=0))
        battle.accept_move(player_two, Move(p4, p1, damage=50))
        battle.accept_move(player_one, Move(p1, p4, damage=100))
        battle.accept_move(player_one, Move(p3, None, move_type=0))
        battle.accept_move(player_two, Move(p4, p3, damage=100))
        battle.accept_move(player_one, Move(p3, p4, damage=100))

if __name__ == '__main__':
    unittest.main()