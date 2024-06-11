from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
from graficos import get_best_team,pokedex_number_dict
from Algoritmo_genetico import leer_datos



def simulated_combat(best_team, team2, effectiveness):
    turn = 0
    while any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):            
        print(f"Turn {turn} has started\n")
        action_1, target_1 = best_team.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(best_team, effectiveness)

        # Switching always happens first
        if action_1 == 'switch':
            first = best_team
            second = team2
        elif action_2 == 'switch':
            first = team2
            second = best_team
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
        # If nobody is switching, the fastest pokemon goes firsts
        elif best_team.get_current_pokemon().speed > team2.get_current_pokemon().speed:
            first = best_team
            second = team2
        else:
            first = team2
            second = best_team
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1

        print(f"{first.name} turn:")
        print(first.do_action(action_1, target_1, second, effectiveness))
        
        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            if best_team.get_current_pokemon().current_hp == 0:
                print(f"{best_team.get_current_pokemon().name} has fainted")
            else:
                print(f"{team2.get_current_pokemon().name} has fainted")
            __faint_change__(best_team, team2, effectiveness)
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)

            print(f"\n{second.name} turn:")
            print(second.do_action(action_2, target_2, first, effectiveness))

            if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                if best_team.get_current_pokemon().current_hp == 0:
                    print(f"{best_team.get_current_pokemon().name} has fainted")
                else:
                    print(f"{team2.get_current_pokemon().name} has fainted")
                __faint_change__(best_team, team2, effectiveness)
        
        print(f"Turn {turn} has ended\n" + "--"*40)
        #print("--"*40)
        turn += 1
        
    print(f"{best_team.name} has won!" if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else f"{team2.name} has won!")
    return best_team if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else team2
    
def pokemon_to_obj(poke_list: list, moves_dict, pokemon_dict, name: str, starter = 0) -> Team:
    dic = pokedex_number_dict()
    team_temp = []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team


def main():
    pokemon_elite_1 = ["Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"]
    pokemon_elite_2 = ["Skuntank", "Toxicroak", "Swalot", "Venomoth", "Muk", "Crobat"]
    pokemon_elite_3 = ["Hitmontop", "Hitmonlee", "Hariyama", "Machamp", "Lucario", "Hitmonchan"]
    pokemon_elite_4 = ["Weavile", "Spiritomb", "Honchkrow", "Umbreon", "Houndoom", "Absol"]
    pokemon_champion = ["Salamence", "Garchomp", "Dragonite", "Charizard", "Altaria", "Gyarados"]
    moves_dict,pokemon_dict,effectiveness_dict = leer_datos()
    team = get_best_team(50)
    best_team = pokemon_to_obj(team[4:], moves_dict, pokemon_dict, "best", int(team[3]))
    elite_1 = pokemon_to_obj(pokemon_elite_1, moves_dict, pokemon_dict, "elite_1")

    elite_2 = pokemon_to_obj(pokemon_elite_2, moves_dict, pokemon_dict, "elite_2")
    elite_3 = pokemon_to_obj(pokemon_elite_3, moves_dict, pokemon_dict, "elite_3")
    elite_4 = pokemon_to_obj(pokemon_elite_4, moves_dict, pokemon_dict, "elite_4")
    champion = pokemon_to_obj(pokemon_champion, moves_dict, pokemon_dict, "champion")

    ganador = simulated_combat(elite_4,champion,effectiveness_dict).pokemons
    
if __name__ == "__main__": 
    main()