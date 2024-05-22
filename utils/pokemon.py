from utils.move import Move, CATEGORIES

TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
TYPES_COLORS = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']

class Pokemon:
    def __init__(
            self,
            pokedex_number: int,
            name: str,
            type1: str,
            type2: str|None,
            hp: int,
            attack: int,
            defense: int,
            sp_attack: int,
            sp_defense: int,
            speed: int,
            generation: int,
            height: float,
            weight: float,
            is_legendary: bool,
            moves: list[Move],
            level: int=50
        ):
        """
        Creates a Pokemon object.
        
        Parameters:
        pokedex_number (int): The pokedex number of the pokemon.
        name (str): The name of the pokemon.
        type1 (str): The primary type of the pokemon.
        type2 (str|None): The secondary type of the pokemon. If the pokemon has only one type, this should be None.
        hp (int): The base hp of the pokemon.
        attack (int): The base attack of the pokemon.
        defense (int): The base defense of the pokemon.
        sp_attack (int): The base special attack of the pokemon.
        sp_defense (int): The base special defense of the pokemon.
        speed (int): The base speed of the pokemon.
        generation (int): The generation of the pokemon.
        height (float): The height of the pokemon in meters.
        weight (float): The weight of the pokemon in kilograms.
        is_legendary (bool): Whether the pokemon is legendary or not.
        moves (list[Move]): The moves that the pokemon can use.
        level (int): The level of the pokemon. Default is 50.
        """

        if type1 == type2:
            raise ValueError('The primary and secondary types of a Pokemon cannot be the same.')
        self.pokedex_number = pokedex_number
        self.name = name
        self.type1 = type1 if type1 != '' else None
        self.type2 = type2 if type2 != '' else None
        self.max_hp = hp * (1 + level/50)
        self.current_hp = self.max_hp
        self.attack = attack * (1 + level/50)
        self.defense = defense * (1 + level/50)
        self.sp_attack = sp_attack * (1 + level/50)
        self.sp_defense = sp_defense * (1 + level/50)
        self.speed = speed * (1 + level/50)
        self.generation = generation
        self.height = height
        self.weight = weight
        self.is_legendary = is_legendary
        self.level = level
        self.moves = moves
        self.__filter_moves__()
        
    @staticmethod
    def from_dict(name: str, data: dict[str, str|int|float|bool|None], moves_data: dict[str, dict[str, str|int]]):
        """
        Creates a Pokemon object from a dictionary.

        Parameters:
        name (str): The name of the pokemon.
        data (dict[str, str|int|float|bool|None]): A dictionary that contains the pokedex number, type1, type2, hp,
        attack, defense, sp_attack, sp_defense, speed, generation, height_m, weight_kg, is_legendary and moves of the
        pokemon.
        moves_data (dict[str, dict[str, str|int]]): A dictionary that contains the data of the moves of the pokemon.

        Returns:
        Pokemon: The pokemon created from the dictionary.

        Example:
        >>> data = {
        ...     'pokedex_number': 1,
        ...     'type1': 'grass',
        ...     'type2': 'poison',
        ...     'hp': 45,
        ...     'attack': 49,
        ...     'defense': 49,
        ...     'sp_attack': 65,
        ...     'sp_defense': 65,
        ...     'speed': 45,
        ...     'generation': 1,
        ...     'height_m': 0.7,
        ...     'weight_kg': 6.9,
        ...     'is_legendary': False,
        ...     'moves': ['tackle', 'growl', 'leer', 'vine whip']
        ... }
        >>> moves_data = {
        ...     'tackle': {'type': 'normal', 'category': 'physical', 'pp': 35, 'power': 40, 'accuracy': 100},
        ...     'growl': {'type': 'normal', 'category': 'status', 'pp': 40, 'power': 0, 'accuracy': 100},
        ...     'leer': {'type': 'normal', 'category': 'status', 'pp': 30, 'power': 0, 'accuracy': 100},
        ...     'vine whip': {'type': 'grass', 'category': 'physical', 'pp': 25, 'power': 45, 'accuracy': 100}
        ... }
        >>> pokemon = Pokemon.from_dict('Bulbasaur', data, moves_data)
        """

        return Pokemon(
            data['pokedex_number'],
            name,
            data['type1'],
            data['type2'],
            data['hp'],
            data['attack'],
            data['defense'],
            data['sp_attack'],
            data['sp_defense'],
            data['speed'],
            data['generation'],
            data['height_m'],
            data['weight_kg'],
            data['is_legendary'],
            [Move.from_dict(move, moves_data[move]) for move in data['moves'] if move != '']
        )
    
    def __filter_moves__(self):
        """
        Filters the moves of the pokemon to only keep the best move of each type and category.
        """
        moves = {}
        
        for type in TYPES:
            moves[type] = {}
            for category in CATEGORIES:
                moves[type][category] = []

                for move in self.moves:
                    if move.type == type and move.category == category:
                        moves[type][category].append((move.power * move.accuracy, move))
                if moves[type][category] == []:
                    moves[type][category] = None
                else:
                    moves[type][category].sort(key=lambda x: x[0], reverse=True)
                    moves[type][category] = moves[type][category][0][1]
        self.moves = moves

    def get_best_attack(self, defending_pokemon: 'Pokemon', effectiveness: dict[str, dict[str, float]]):
        """
        Returns the best move of the pokemon against the defending pokemon.

        Parameters:
        defending_pokemon (Pokemon): The pokemon that will receive the move.
        effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
        another.

        Returns:
        Move: The best move of the pokemon against the defending pokemon.
        float: The damage that the move would do to the defending pokemon.
        """
        best_move = None
        best_damage = 0
        for type in self.moves:
            for category in self.moves[type]:
                move = self.moves[type][category]
                if move is not None:
                    damage = move.get_damage(self, defending_pokemon, effectiveness)
                    if damage > best_damage:
                        best_damage = damage
                        best_move = move
        return best_move, best_damage
