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

        self.assertTrue(battle.team_a.is_defeated())

    def test_two_vs_two(self):
        SystemManager.get_instance().init([
            BattleSystem()
        ])

        player_one = Player(0, 0, 0, 'player one', None)
        player_two = Player(0, 0, 0, 'player two', None)
        player_three = Player(0, 0, 0, 'player three', None)
        player_four = Player(0, 0, 0, 'player four', None)

        p1 = Pokemon(player_one)
        p2 = Pokemon(player_two)
        p3 = Pokemon(player_three)
        p4 = Pokemon(player_four)
        p5 = Pokemon(player_three)

        team_a_settings = {
            'lineups': [[p1], [p2]],
            'size': 2
        }

        team_b_settings = {
            'lineups': [[p3, p5], [p4]],
            'size': 2
        }

        battle = Battle(
            team_a_settings,
            team_b_settings, 
            [player_one, player_two, player_three, player_four]
        )

        battle.accept_move(player_one, Move(p1, p3, damage=50))
        battle.accept_move(player_two, Move(p2, p3, damage=50))
        battle.accept_move(player_three, Move(p3, p2, damage=50))
        battle.accept_move(player_four, Move(p4, p1, damage=50))

        battle.accept_move(player_three, Move(p5, None, move_type=0))

        battle.accept_move(player_one, Move(p1, p4, damage=50))
        battle.accept_move(player_two, Move(p2, p4, damage=50))
        battle.accept_move(player_four, Move(p4, p1, damage=50))
        battle.accept_move(player_three, Move(p5, p1, damage=50))

        battle.accept_move(player_two, Move(p2, p5, damage=100))
        battle.accept_move(player_three, Move(p5, p2, damage=100))

        self.assertTrue(battle.team_b.is_defeated())

if __name__ == '__main__':
    unittest.main()
