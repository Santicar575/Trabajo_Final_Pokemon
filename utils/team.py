import copy

from utils.pokemon import Pokemon
from utils.move import Move

class Team:
    def __init__(self, name: str, pokemons: list[Pokemon], starter: int=0):
        """
        Creates a Team object.
        
        Parameters:
        name (str): The name of the team.
        pokemons (list[Pokemon]): The pokemons that the team has.
        starter (int): The index of the pokemon that starts the battle. Default is 0.
        """
        if len(pokemons) > 6:
            raise ValueError('A team can have at most 6 pokemons')
        if len(set(pokemon.name for pokemon in pokemons)) < len(pokemons):
            raise ValueError('A team cannot have two pokemons with the same name')
        self.name = name
        self.pokemons = [copy.deepcopy(pokemon) for pokemon in pokemons]
        self.current_pokemon_index = starter
        self.consecutive_switches = 0

    def get_current_pokemon(self) -> Pokemon:
        """
        Returns the current pokemon of the team.
        
        Returns:
        Pokemon: The current pokemon of the team."""
        return self.pokemons[self.current_pokemon_index]

    def change_pokemon(self, index: int) -> None:
        """
        Changes the current pokemon of the team.

        Parameters:
        index (int): The index of the pokemon that will become the current pokemon.
        """
        if index < len(self.pokemons) and self.pokemons[index].current_hp > 0:
            self.current_pokemon_index = index
        else:
            raise ValueError('Invalid pokemon index')

    def recieve_damage(self, damage: float) -> None:
        """
        Reduces the current hp of the current pokemon by the damage.

        Parameters:
        damage (float): The damage that the pokemon will receive.
        """
        self.get_current_pokemon().current_hp -= damage
        if self.get_current_pokemon().current_hp <= 0:
            self.get_current_pokemon().current_hp = 0

    def get_next_action(self, defending_team: 'Team', effectiveness: dict[str, dict[str, float]]) -> tuple[str, Move|int|None]:
        """
        Returns the next action that the team will do.

        Parameters:
        defending_team (Team): The team that the team will attack.
        effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
        another.

        Returns:
        str: The action that the team will do. It can be 'attack', 'switch' or 'skip'.
        Move|int|None: The move that the team will use if the action is 'attack', the index of the pokemon that the team
        will switch to if the action is 'switch' or None if the action is 'skip'.
        """
        best_pokemon_i = None
        best_damage = 0
        best_move = None
        for i, pokemon in enumerate(self.pokemons):
            if pokemon.current_hp > 0:
                if best_pokemon_i is None:
                    best_pokemon_i = i
                move, damage = pokemon.get_best_attack(defending_team.get_current_pokemon(), effectiveness)
                if damage > best_damage or best_move is None:
                    best_damage = damage
                    best_pokemon_i = i
                    best_move = move
    
        if self.get_current_pokemon().current_hp == 0:
            return 'switch', best_pokemon_i
        elif best_move is None:
            return 'skip', None
        
        current_move, current_damage = self.get_current_pokemon().get_best_attack(defending_team.get_current_pokemon(), effectiveness)
        if current_damage > defending_team.get_current_pokemon().current_hp:
            return 'attack', current_move
        elif (best_pokemon_i != self.current_pokemon_index) and self.consecutive_switches < 10:
            return 'switch', best_pokemon_i
        else:
            return 'attack', best_move


    def do_action(self, action: str, target: Move|int|None, defender: 'Team', effectiveness: dict[str, dict[str, float]]) -> None:
        """
        Executes an action.

        Parameters:
        action (str): The action that the team will do. It can be 'attack' or 'switch'.
        target (Move|int|None): The move that the team will use if the action is 'attack', the index of the pokemon that
        the team will switch to if the action is 'switch' or None if the action is 'skip'.
        defender (Team): The team that will receive the action.
        effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
        another.
        """
        if action == 'attack':
            damage = target.get_damage(self.get_current_pokemon(), defender.get_current_pokemon(), effectiveness)
            defender.recieve_damage(damage)
            self.consecutive_switches = 0
        elif action == 'switch':
            if target is not None:
                self.change_pokemon(target)
                self.consecutive_switches += 1
        else:
            self.get_current_pokemon().current_hp = 0
