from collections import defaultdict
from lanturn.ecs.component.battle import BattleComponent
from lanturn.battle.arena import Arena
from lanturn.battle.ai import BattleAI
from lanturn.battle.team import Team

class FaintSubstituteBattleState(object):
    def __init__(self, battle):
        self.battle = battle
        self.setup([])

    def setup(self, fainted_pokemon):
        self.substitute_selection = defaultdict(list)
        self.num_required_substitutes = defaultdict(int)

        for pokemon in fainted_pokemon:
            self.num_required_substitutes[pokemon.owner] += 1

            # Cap off the number of required substitutes by the number
            # of healthy pokemon in the pokemon's lineup
            self.num_required_substitutes[pokemon.owner] = min(
                self.num_required_substitutes[pokemon.owner],
                len(pokemon[BattleComponent].team.pokemon_to_lineup[pokemon].healthy_pokemon)
            )

        return sum(self.num_required_substitutes.values()) > 0

    def accept_move(self, player, move):
        if move.type != 0:
            print 'Received an invalid move while in faint state'
            return self

        pokemon = move.source

        # Verify that the pokemon is not already in the active set
        if pokemon in pokemon[BattleComponent].team.active:
            print 'Pokemon already part of the active set'
            return self

        # Verify that the player is not making more substitutions than necessary
        if len(self.substitute_selection[player]) >= self.num_required_substitutes[player]:
            print 'Player has already selected their required number of substitutes'
            return self

        pokemon[BattleComponent].team.active.add(move.source)
        self.substitute_selection[player].append(pokemon)

        # Check if we meet the number of required substitutes
        if sum(len(selection) for selection in self.substitute_selection.values()) \
          < sum(self.num_required_substitutes.values()):
            return self

        for player, pokemon in self.substitute_selection.items():
            print '{} selected {} for substitution'.format(
                player, ', '.join(map(lambda x: str(x), pokemon))
            )

        # TODO: Inform players of substitutions

        # Reinitialize the combat state
        self.battle.battle_states['combat'].setup()
        return self.battle.battle_states['combat']

class CombatBattleState(object):
    def __init__(self, battle, team_a, team_b, players):
        self.battle = battle
        self.team_a = team_a
        self.team_b = team_b
        self.players = players

        self.arena = Arena()
        self.battle_ai = BattleAI()
        self.setup()

    def setup(self):
        self.waiting_for_moves = defaultdict(int)
        self.moves = []
        for pokemon in self.get_active():
            if pokemon.owner != None:
                self.waiting_for_moves['{}_{}'.format(pokemon.owner.id, pokemon.id)] = 1

    def get_active(self):
        active_pokemon = set()
        active_pokemon.update(self.team_a.get_active())
        active_pokemon.update(self.team_b.get_active())
        return active_pokemon

    def accept_move(self, player, move):
        if move.type != 1:
            print 'Received an invalid move while in combat state'
            return self

        if self.waiting_for_moves['{}_{}'.format(move.source.owner.id, move.source.id)] == 1:
            self.waiting_for_moves['{}_{}'.format(move.source.owner.id, move.source.id)] -= 1
            self.moves.append(move)

        # Check if we've received moves for each player
        # owned pokemon in the active set
        if sum(self.waiting_for_moves.values()) > 0:
            return self

        active_pokemon = self.get_active()
        for pokemon in active_pokemon:
            if pokemon.owner == None:
                self.moves.append(self.battle_ai.generate_move(pokemon))

        fainted_pokemon = self.arena.evaluate_round(self.moves, active_pokemon)

        for pokemon in fainted_pokemon:
            team = pokemon[BattleComponent].team 
            team.fainted(pokemon)
            if team.has_substitute(pokemon):
                if pokemon.owner is None:
                    pass
                    # TODO: AI select a substitute

                # For the player case, the client is expected
                # to know to send a substitution message to
                # the server
            else:
                print 'NO SUBSTITUTE AVAILABLE'
                if team.is_defeated():
                    print 'TEAM DEFEATED'

        player_owned_fainted_pokemon = [pokemon for pokemon in fainted_pokemon if pokemon.owner]
        if player_owned_fainted_pokemon:
            if self.battle.battle_states['faint'].setup(player_owned_fainted_pokemon):
                return self.battle.battle_states['faint']

        # TODO: send information to players

        # Initialize next round of combat
        self.setup()
        return self

class Battle(object):
    def __init__(self, team_a_settings, team_b_settings, players):
        self.players = players
        self.team_a = self._setup_team(team_a_settings)
        self.team_b = self._setup_team(team_b_settings)
        self._setup_battle_components(self.team_a, self.team_b)
        self._setup_battle_components(self.team_b, self.team_a)

        self.battle_states = {
            'faint': FaintSubstituteBattleState(self),
            'combat': CombatBattleState(self, self.team_a, self.team_b, players)
        }
        self.battle_state = self.battle_states['combat']

    def _setup_team(self, settings):
        size = settings['size']
        lineups = settings['lineups']
        team = Team(size, lineups)
        return team

    def _setup_battle_components(self, team, opposing_team):
        for lineup in team.lineups:
            for pokemon in lineup.pokemon():
                pokemon.add_component(BattleComponent(pokemon, team, opposing_team))

    def accept_move(self, player, move):
        # Verify that the pokemon is part of the player's lineup
        pokemon = move.source
        if pokemon not in pokemon[BattleComponent].team.player_to_lineup[player].pokemon():
            print 'Pokemon not part of the owner\'s lineup'
            return

        self.battle_state = self.battle_state.accept_move(player, move)
