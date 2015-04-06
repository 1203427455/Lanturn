import random
from lanturn.ecs.component.battle import BattleComponent

class Team(object):
    def __init__(self, size, lineups):
        self.size = size
        self.active = set()
        self.lineups = lineups

        if size % len(self.lineups) != 0:
            raise Exception('team size must be divisible by the number of lineups')

        for i, lineup in enumerate(self.lineups):
            for j in range(self.size / len(lineups)):
                self.active.add(lineup[j])

    def get_active(self):
        return self.active

class Move(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def execute(self):
        self.target.health -= random.randint(1, 100)

class Arena(object):
    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b

    def get_active(self):
        active_pokemon = set()
        active_pokemon.update(self.team_a.get_active())
        active_pokemon.update(self.team_b.get_active())
        return active_pokemon

    def evaluate_round(self, moves):
        active_pokemon = self.get_active()

        # TODO: sort by move priority + pokemon speed

        for move in moves:
            if move.source in active_pokemon:
                if move.target in active_pokemon:
                    move.execute()
                    if move.target.health <= 0:
                        move.target.health = 0
                        active_pokemon.remove(move.target)
                        move.source[BattleComponent].opposing_team.active.remove(move.target)
                else:
                    available_targets = list(move.source[BattleComponent].opposing_team.get_active())
                    if len(available_targets) > 0:
                        move.target = available_targets[random.randint(0, len(available_targets) - 1)]
                        move.execute()

