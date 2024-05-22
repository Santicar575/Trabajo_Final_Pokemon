import random

CATEGORIES = ['physical', 'special']

class Move:
    def __init__(self, name: str, type: str, category: str, pp: int, power: int, accuracy: int):
        self.name = name
        self.type = type
        self.category = category
        self.pp = pp
        self.power = power
        self.accuracy = accuracy

    @staticmethod
    def from_dict(name: str, data: dict[str, str|int]):
        """
        Creates a Move object from a dictionary.
        
        Parameters:
        name (str): The name of the move.
        data (dict[str, str|int]): A dictionary that contains the type, category, pp, power and accuracy of the move.
        
        Returns:
        Move: The move created from the dictionary.
        
        Example:
        >>> data = {'type': 'fire', 'category': 'special', 'pp': 10, 'power': 90, 'accuracy': 100}
        >>> move = Move.from_dict('Flamethrower', data)
        """
        return Move(
            name,
            data['type'],
            data['category'],
            data['pp'],
            data['power'],
            data['accuracy']
        )
    
    def get_damage(self, attacker_pokemon: 'Pokemon', defending_pokemon: 'Pokemon', effectiveness: dict[str, dict[str, float]]) -> float:
        """
        Calculates the damage that the move would do to the defending pokemon.

        Parameters:
        attacker_pokemon (Pokemon): The pokemon that uses the move.
        defending_pokemon (Pokemon): The pokemon that receives the move.
        effectiveness (dict[str, dict[str, float]]): A dictionary that contains the effectiveness of each type against
        another.

        Returns:
        float: The damage that the move would do to the defending pokemon.
        """
        if self.accuracy < random.random():
            return 0
        if self.category == 'physical':
            a = attacker_pokemon.attack
            d = defending_pokemon.defense
        else:
            a = attacker_pokemon.sp_attack
            d = defending_pokemon.sp_defense

        stab = 1.5 if self.type == attacker_pokemon.type1 or self.type == attacker_pokemon.type2 else 1
        effectiveness_bonus = effectiveness[defending_pokemon.type1][self.type]
        if defending_pokemon.type2 is not None:
            effectiveness_bonus *= effectiveness[defending_pokemon.type2][self.type]

        return (((2*attacker_pokemon.level/5) * self.power * a/d)/50 + 2) * stab * effectiveness_bonus
