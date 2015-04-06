from lib.ecs.component.component import Component

class BattleComponent(Component):
    component_id = 'BattleComponent'

    def __init__(self, pokemon, team, opposing_team):
    	self.pokemon = pokemon
    	self.team = team
    	self.opposing_team = opposing_team
