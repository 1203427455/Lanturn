import random
from lanturn.ecs.component.battle import BattleComponent
from lanturn.battle.move import Move

class BattleAI(object):
    def generate_move(self, pokemon):
        foes = list(pokemon[BattleComponent].opposing_team.get_active())
        target = foes[random.randint(0, len(foes)-1)]    
        return Move(pokemon, target)
