from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
from graficos import get_best_team,pokedex_number_dict
from Algoritmo_genetico import leer_datos
import pygame
import sys
import time 


def simulated_combat_gui(best_team, team2, effectiveness,pokemon_dict,pokedex_dict):
    # Create a new window
    pygame.init()
    
    # Set the size of the window
    screen = pygame.display.set_mode((772, 518))

    # Set the title of the window
    pygame.display.set_caption("Pokemon Battle")

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Create a list to store the battle log
    battle_log = []
    battle_log_mia= [ ]

    #Create the backgroound for the window
    background = pygame.image.load("background.jpg").convert()
    turn = 0
    
    while any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):            
        battle_log_temp = []
        battle_log_temp.append(f"Turn {turn} has started")
        action_1, target_1 = best_team.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(best_team, effectiveness)
        poke1 = best_team.get_current_pokemon()
        poke2 = team2.get_current_pokemon()
        
       
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
            
        
        # battle_log_temp.append(f"{first.name} turn:")
        # battle_log_temp.append(first.get_next_action(action_1, target_1, second, effectiveness))
        # battle_log_temp.append({first.name: [first.get_current_pokemon().name,first.get_current_pokemon().current_hp], second.name: [second.get_current_pokemon().name,second.get_current_pokemon().current_hp]})
        
        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            if best_team.get_current_pokemon().current_hp == 0:
                battle_log_temp.append(f"{best_team.get_current_pokemon().name} has fainted")
            else:
                battle_log_temp.append(f"{team2.get_current_pokemon().name} has fainted")
            __faint_change__(best_team, team2, effectiveness)
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)

            battle_log_temp.append(f"{second.name} turn:")
            battle_log_temp.append(second.return_action(action_2, target_2, first, effectiveness))

            if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                if best_team.get_current_pokemon().current_hp == 0:
                    battle_log_temp.append(f"{best_team.get_current_pokemon().name} has fainted")
                else:
                    battle_log_temp.append(f"{team2.get_current_pokemon().name} has fainted")
                __faint_change__(best_team, team2, effectiveness)

      
        battle_log_temp.append({best_team.name: [best_team.get_current_pokemon().name,best_team.get_current_pokemon().current_hp], team2.name: [team2.get_current_pokemon().name,team2.get_current_pokemon().current_hp]})
        # battle_log_temp.append(f"Turn {turn} has ended" )
        battle_log.append(battle_log_temp)
        battle_log_mia.append({"first": (first,action_1,target_1,[first.get_current_pokemon().name,first.get_current_pokemon().current_hp],poke1), "second": (second,action_2,target_2,[second.get_current_pokemon().name,second.get_current_pokemon().current_hp],poke2)})
        turn += 1
        
    
    # Display who won
    winner = best_team if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else team2
    battle_log.append([f"{winner.name} has won!"])
    lista_imagenes =[]
    for pokemon in winner.pokemons: 
        pokemon = pokedex_dict[pokemon.name].zfill(3)
        lista_imagenes.append(pygame.image.load(f'data/imgs/{pokemon}.png'))







    screen.blit(background,[0,0])
    pokemon1 = pokedex_dict[best_team.get_current_pokemon().name].zfill(3)
    pokemon2 = pokedex_dict[team2.get_current_pokemon().name].zfill(3)
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))

    #LOG
    rectangle = pygame.Rect(30, 450, 680, 65) 
    text = "Inicio de batalla!!!"
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    # Dibujar el texto en la pantalla
    screen.blit(text_surface, (60, 470))
    pygame.display.flip()
    
    #POKEMON AMIGO
    rectangle_amigo = pygame.Rect(457, 317, 195, 20) 
    texto = best_team.get_current_pokemon().name
    text_amigo = font.render(texto, True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), rectangle_amigo)
    # Dibujar el texto en la pantalla
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle_amigo.x + rectangle_amigo.width - text_width, rectangle_amigo.y + (rectangle_amigo.height - text_height) // 2))
    pygame.display.flip()


    #POKEMON ENEMIGO
    rectangle_enemigo = pygame.Rect(20, 90, 190, 20) 
    texto = team2.get_current_pokemon().name
    text_enemigo = font.render(texto, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle_enemigo)
    # Dibujar el texto en la pantalla
    text_width = text_enemigo.get_width()
    text_height = text_enemigo.get_height()
    screen.blit(text_enemigo, (rectangle_enemigo.x + rectangle_enemigo.width - text_width, rectangle_enemigo.y + (rectangle_enemigo.height - text_height) // 2))
    pygame.display.flip()
    
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
      
        for turn in battle_log_mia: 
            if action_1 == "switch":
                pokemon1 = pokedex_dict[turn[4][0]].zfill(3)
                equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1}.png'),(200,200))
                equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2}.png'),(200,200))
                screen.blit(equipo1_pokemon_image, (100, 225))
                screen.blit(equipo2_pokemon_image, (500, 105))
                text = f"{turn[0].name} was {} to {pokemon1} "
                pygame.display.flip()
            elif action_1 == "attack": 
                pass




                


       
    # # Run the GUI loop
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #     # put backgrpund 
    #     screen.blit(background,[0, 0])
        
    #     # Draw the battle log
    #     for turn in battle_log:
    #         print(turn)
    #         pokemon1 = pokedex_dict[best_team.get_current_pokemon().name].zfill(3)
    #         pokemon2 = pokedex_dict[team2.get_current_pokemon().name].zfill(3)
    #         equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1}.png'),(200,200))
    #         equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2}.png'),(200,200))
    #         screen.blit(equipo1_pokemon_image, (100, 270))
    #         screen.blit(equipo2_pokemon_image, (500, 105))
    #         screen.blit(background,[0, 0])
    #         pygame.display.flip()
    #         for i,line in enumerate(turn):

    #             if type(line) == dict:
    #                 pokemon1 = pokedex_dict[line[best_team.name][0]].zfill(3)
    #                 pokemon2 = pokedex_dict[line[team2.name][0]].zfill(3)
                    
    #                 equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1}.png'),(200,200))
    #                 equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2}.png'),(200,200))
    #                 screen.blit(equipo1_pokemon_image, (100, 270))
    #                 screen.blit(equipo2_pokemon_image, (500, 105))
    #                 pass
    #             else:
    #                 text = font.render(line, True, (255, 255, 255))
    #                 screen.blit(text, (20, 20 + i*40))
    #         while True:
    #             next_turn = False
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.quit()
    #                     sys.exit()
    #                 if event.type == pygame.KEYDOWN:
    #                     screen.blit(background,[0, 0])
    #                     next_turn = True
    #                     break
    #             if next_turn:
    #                 break
    #             pygame.display.flip()
                
    #     pygame.quit()
    #     sys.exit()
    
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
    agus_team = ["Bouffalant","Delphox","Mamoswine","Tsareena","Greninja","Slaking"]
    moves_dict,pokemon_dict,effectiveness_dict = leer_datos()
    pokedex_dict = pokedex_number_dict()
    team = get_best_team(50)
    best_team = pokemon_to_obj(team[4:], moves_dict, pokemon_dict, "best", int(team[3]))
    elite_1 = pokemon_to_obj(pokemon_elite_1, moves_dict, pokemon_dict, "elite_1")
    elite_2 = pokemon_to_obj(pokemon_elite_2, moves_dict, pokemon_dict, "elite_2")
    elite_3 = pokemon_to_obj(pokemon_elite_3, moves_dict, pokemon_dict, "elite_3")
    elite_4 = pokemon_to_obj(pokemon_elite_4, moves_dict, pokemon_dict, "elite_4")
    champion = pokemon_to_obj(pokemon_champion, moves_dict, pokemon_dict, "champion")
    agus_team = pokemon_to_obj(agus_team, moves_dict, pokemon_dict, "Agus_team",0)

    ganador = simulated_combat_gui(best_team,agus_team,effectiveness_dict,pokemon_dict,pokedex_dict).pokemons
    
if __name__ == "__main__": 
    main()