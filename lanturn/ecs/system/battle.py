import json
import random
from collections import defaultdict
from lib.ecs.system.system import System
from lanturn.ecs.message_types import MESSAGE_TYPE
from lanturn.ecs.component.replication import ReplicationComponent
from lanturn.arena import Arena, Team, Move
from lanturn.ecs.component.battle import BattleComponent

class BattleAI(object):
    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b

    def generate_move(self, pokemon):
        foes = list(pokemon[BattleComponent].opposing_team.get_active())
        target = foes[random.randint(0, len(foes)-1)]    
        return Move(pokemon, target)

class Battle(object):
    def __init__(self, team_a, team_b, players):
        self.arena = Arena(team_a, team_b)
        self.moves = []
        self.battle_ai = BattleAI(team_a, team_b)
        self.setup()

    def setup(self):
        active_pokemon = self.arena.get_active()
        self.waiting_for_moves = defaultdict(int)
        self.moves = []
        for pokemon in active_pokemon:
            if pokemon.owner != None:
                self.waiting_for_moves['{}_{}'.format(pokemon.owner.id, pokemon.id)] = 1

    def accept_move(self, player, move):
        if self.waiting_for_moves['{}_{}'.format(move.source.owner.id, move.source.id)] == 1:
            self.waiting_for_moves['{}_{}'.format(move.source.owner.id, move.source.id)] -= 1
            self.moves.append(move)

        if sum(self.waiting_for_moves.values()) > 0:
            return

        active_pokemon = self.arena.get_active()
        for pokemon in active_pokemon:
            if pokemon.owner == None:
                self.moves.append(self.battle_ai.generate_move(pokemon))

        self.arena.evaluate_round(self.moves)

        for pokemon in active_pokemon:
            print pokemon.id, pokemon.health

        self.setup()

class BattleSystem(System):
    def __init__(self):
        message_handlers = {
            MESSAGE_TYPE.CREATE_BATTLE: self.handle_create_battle,
            MESSAGE_TYPE.PLAYER_BATTLE_MOVE: self.handle_player_battle_move,
        }
        self.player_to_battle = {}

        super(BattleSystem, self).__init__(message_handlers)

    def _setup_team(self, settings):
        size = settings['size']
        lineups = settings['lineups']
        team = Team(size, lineups)
        return team

    def _setup_battle_components(self, team, opposing_team):
        for lineup in team.lineups:
            for pokemon in lineup:
                pokemon.add_component(BattleComponent(pokemon, team, opposing_team))

    def handle_player_battle_move(self, message):
        player = message['player']
        pokemon = message['pokemon']
        battle = self.player_to_battle[player]
        battle.accept_move(player, battle.battle_ai.generate_move(pokemon))

    def handle_create_battle(self, message):
        team_a = self._setup_team(message['team_a_settings'])
        team_b = self._setup_team(message['team_b_settings'])
        self._setup_battle_components(team_a, team_b)
        self._setup_battle_components(team_b, team_a)

        players = message['players']
        battle = Battle(team_a, team_b, players)
        for player in players:
            self.player_to_battle[player] = battle

    def update(self, delta):
        self.handle_messages()