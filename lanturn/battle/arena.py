import random
from lanturn.ecs.component.battle import BattleComponent

class Arena(object):
    def evaluate_round(self, moves, active_pokemon):
        fainted = set()
        # TODO: sort by move priority + pokemon speed

        for move in moves:
            if move.source in active_pokemon:
                if move.target not in active_pokemon:
                    available_targets = list(move.target[BattleComponent].team.get_active())
                    if len(available_targets) > 0:
                        target_index = random.randint(0, len(available_targets) - 1)
                        move.target = available_targets[target_index]
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


