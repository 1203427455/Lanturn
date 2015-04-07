import random
from collections import OrderedDict
from lanturn.ecs.component.battle import BattleComponent

class Lineup(object):
    def __init__(self, lineup):
        self.lineup = lineup
        self.healthy_pokemon = OrderedDict()
        self.fainted_pokemon = OrderedDict()

        for pokemon in lineup:
            if pokemon.health > 0:
                self.healthy_pokemon[pokemon] = True
            else:
                self.fainted_pokemon[pokemon] = True

    def fainted(self, pokemon):
        if pokemon in self.healthy_pokemon:
            self.healthy_pokemon.pop(pokemon)

        self.fainted_pokemon[pokemon] = True

    def pokemon(self):
        return self.lineup

    def get_starters(self, size):
        starters = set()
        for pokemon in self.healthy_pokemon.keys():
            starters.add(pokemon)
            if len(starters) == size:
                break
        return starters

class Team(object):
    def __init__(self, size, lineups):
        self.size = size
        self.active = set()
        self.lineups = [Lineup(lineup) for lineup in lineups]
        self.pokemon_to_lineup = {}
        self.player_to_lineup = {}

        if size % len(self.lineups) != 0:
            raise Exception('team size must be divisible by the number of lineups')

        for lineup in self.lineups:
            for pokemon in lineup.pokemon():
                # Configure mappings to lineups
                self.pokemon_to_lineup[pokemon] = lineup
                if pokemon.owner is not None:
                    self.player_to_lineup[pokemon.owner] = lineup

        num_starters = self.size / len(lineups)
        for lineup in self.lineups:
            starters = lineup.get_starters(num_starters)
            self.active.update(starters)

    def get_active(self):
        return self.active

    def fainted(self, pokemon):
        self.pokemon_to_lineup[pokemon].fainted(pokemon)
        if pokemon in self.active:
            self.active.remove(pokemon)

    def is_defeated(self):
        return sum(len(lineup.healthy_pokemon) for lineup in self.lineups) == 0

    def has_substitute(self, pokemon):
        lineup = self.pokemon_to_lineup[pokemon]

        if len(lineup.healthy_pokemon) == 1:
            return pokemon not in lineup.healthy_pokemon
        else:
            return len(lineup.healthy_pokemon) > 1

class Move(object):
    def __init__(self, source, target, move_type=1, damage=None):
        self.source = source
        self.target = target
        self.type = move_type
        self.damage = random.randint(1, 100) if damage is None else damage

    def execute(self):
        self.target.health -= self.damage

class Arena(object):
    def post_execute(self, pokemon, fainted, active_pokemon):
        if pokemon.health <= 0:
            pokemon.health = 0
            fainted.add(move.target)
            active_pokemon.remove(move.target)
            pokemon[BattleComponent].team.active.remove(pokemon)

    def evaluate_round(self, moves, active_pokemon):
        fainted = set()
        # TODO: sort by move priority + pokemon speed

        for move in moves:
            if move.source in active_pokemon:
                if move.target not in active_pokemon:
                    available_targets = list(move.target[BattleComponent].team.get_active())
                    if len(available_targets) > 0:
                        move.target = available_targets[random.randint(0, len(available_targets) - 1)]
                    else:
                        continue

                move.execute()
                print '{} did {} damage to {}'.format(move.source, move.damage, move.target)
                if move.target.health <= 0:
                    print '{} fainted'.format(move.target)
                    move.target.health = 0
                    fainted.add(move.target)
                    active_pokemon.remove(move.target)

        return fainted


