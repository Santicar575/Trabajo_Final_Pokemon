from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
from graficos import get_best_team,pokedex_number_dict
from Algoritmo_genetico import leer_datos
import pygame, sys, time 


def simulated_fight(best_team, team2, effectiveness,pokemon_dict,pokedex_dict,moves_data):
    battle_log = []
    battle_log_mia= []
    turn = 0    
    while any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):            
        battle_log_temp = []
        battle_log_temp.append(f"Turn {turn} has started")
        action_1, target_1 = best_team.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(best_team, effectiveness)
        poke1 = best_team.get_current_pokemon()
        poke2 = team2.get_current_pokemon()
        faint1 = 0 
        faint2 = 0 
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

        movimeinto1 = first.return_action(action_1, target_1, second, effectiveness) 
        # battle_log_temp.append(f"{first.name} turn:")
        # battle_log_temp.append(first.get_next_action(action_1, target_1, second, effectiveness))
        # battle_log_temp.append({first.name: [first.get_current_pokemon().name,first.get_current_pokemon().current_hp], second.name: [second.get_current_pokemon().name,second.get_current_pokemon().current_hp]})
        

        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            if best_team.get_current_pokemon().current_hp == 0:
                faint1 = 1 
                battle_log_temp.append(f"{best_team.get_current_pokemon().name} has fainted")
            else:
                faint2 =  1 
                battle_log_temp.append(f"{team2.get_current_pokemon().name} has fainted")
            __faint_change__(best_team, team2, effectiveness)
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)
            movimeinto2 = second.return_action(action_2, target_2, first, effectiveness) 
            # battle_log_temp.append(f"{second.name} turn:")
            # battle_log_temp.append(second.return_action(action_2, target_2, first, effectiveness))

            if best_team.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                if best_team.get_current_pokemon().current_hp == 0:
                    faint1 =1 
                    battle_log_temp.append(f"{best_team.get_current_pokemon().name} has fainted")
                else:
                    battle_log_temp.append(f"{team2.get_current_pokemon().name} has fainted")
                    faint2 = 1
                __faint_change__(best_team, team2, effectiveness)

   
        battle_log_temp.append({best_team.name: [best_team.get_current_pokemon().name,best_team.get_current_pokemon().current_hp], team2.name: [team2.get_current_pokemon().name,team2.get_current_pokemon().current_hp]})
        # battle_log_temp.append(f"Turn {turn} has ended" )
        battle_log.append(battle_log_temp)
        battle_log_mia.append({"first": (first,action_1,target_1,[first.get_current_pokemon().name,first.get_current_pokemon().current_hp],poke1,movimeinto1,faint1), "second": (second,action_2,target_2,[second.get_current_pokemon().name,second.get_current_pokemon().current_hp],poke2,movimeinto2,faint2)})
        turn += 1
        

    #Display who won
    winner = best_team if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else team2
    #battle_log_mia.append(winner)
    battle_log.append([f"{winner.name} has won!"])
    return battle_log_mia 

def simulated_combat_gui(best_team, team2, effectiveness,pokemon_dict,pokedex_dict,moves_data,battel_log):
    # Create a new window
    pygame.init()
    
    # Set the size of the window
    screen = pygame.display.set_mode((772, 518))

    # Set the title of the window
    pygame.display.set_caption("Pokemon Battle")

    # Create a font object
    font = pygame.font.Font(None, 36)

    # #Create the backgroound for the window
    background = pygame.image.load("background.jpg").convert()
   

    screen.blit(background,[0,0])
    pokemon1_number = pokedex_dict[best_team.get_current_pokemon().name].zfill(3) # numero de pokedex
    pokemon2_number = pokedex_dict[team2.get_current_pokemon().name].zfill(3)
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1_number}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2_number}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))

    #LOG
    rectangle = pygame.Rect(30, 450, 680, 65) 
    text = "Inicio de batalla!!!"
    
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    # Dibujar el texto en la pantalla
    screen.blit(text_surface, (60, 470))
    pygame.display.update()
    
    #POKEMON AMIGO
    poke_amigo = best_team.get_current_pokemon().name
    texto_amigo = font.render(poke_amigo, True, (0, 0, 0))
    Pokemon_Amigo(screen, texto_amigo)

    #POKEMON ENEMIGO
    poke_enemigo = team2.get_current_pokemon().name
    texto_enemigo = font.render(poke_enemigo, True, (0, 0, 0))
    Pokemon_Enemigo(screen, texto_enemigo)    

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
      
        for turn in battel_log:
            if type(turn) == object:
                break  

            if turn["first"][1] == "switch":
                time.sleep(2)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if turn['first'][0] == best_team: 
                    pokemon1_number = int(pokedex_dict[turn['first'][3][0]])  # pokemon podex number
                    pokemon1 = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]
                    pokemon2 = turn['second'][4] #current pokemon at that time as an object
                    pokemon2_number = int(pokedex_dict[pokemon2.name])
                else: 
                    pokemon2_number = int(pokedex_dict[turn['first'][3][0]]) # pokemon podex number
                    pokemon2 = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]
                    pokemon1 = turn['second'][4] #current pokemon at that time as an object
                    pokemon1_number = int(pokedex_dict[pokemon1.name])
                imprimir(screen,pokemon1_number,pokemon2_number)                  
   
                #texto de accion
            
                text = f"{turn["first"][0].name} change {turn["first"][4].name} to {pokemon_dict[pokemon1_number]['name']} "
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))

                #POKEMON AMIGO
                texto = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]['name']
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]['name']
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
               

            elif turn['first'][1] == "attack": 
                time.sleep(2)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if turn['first'][0] == best_team: 
                    pokemon1 = turn['first'][4] #current pokemon at that time  
                    pokemon1_number = int(pokedex_dict[pokemon1.name]) # pokemon podex number
                    pokemon2 = turn['second'][4]
                    pokemon2_number = int(pokedex_dict[pokemon2.name])
                else: 
                    pokemon2 = turn['first'][4] #current pokemon at that time  
                    pokemon2_number = int(pokedex_dict[pokemon2.name]) # pokemon podex number
                    pokemon1 = turn['second'][4]
                    pokemon1_number = int(pokedex_dict[pokemon1.name])
                imprimir(screen,pokemon1_number,pokemon2_number)
            
                #POKEMON AMIGO
                texto = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]['name']
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]['name']
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
               
                #textp de accion 
                text=  turn['first'][5]
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))
                pygame.display.update()

                if turn["second"][6]: 
                    screen.blit(background,[0,0])
                    imprimir(screen,pokemon1_number,pokemon2_number)
                    pygame.display.update()
                    text=  f"{pokemon2.name} has fainted"
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

        

            elif turn['first'][1] == 'skip': 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    text=  f"{turn['first'][0].name} has skip his turn"
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

            if turn['second'][1] == 'switch': 
                time.sleep(2)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if turn['second'][0] == best_team: 
                    pokemon1_number = int(pokedex_dict[turn['second'][3][0]])  # pokemon podex number
                    pokemon1 = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]
                    pokemon2 = turn['first'][4] #current pokemon at that time as an object
                    pokemon2_number = int(pokedex_dict[pokemon2.name])
                else: 
                    pokemon2_number = int(pokedex_dict[turn['second'][3][0]]) # pokemon podex number
                    pokemon2 = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]
                    pokemon1 = turn['first'][4] #current pokemon at that time as an object
                    pokemon1_number = int(pokedex_dict[pokemon1.name])
                imprimir(screen,pokemon1_number,pokemon2_number)                  
   
                #texto de accion
                text = f"{turn["second"][0].name} change {turn["second"][4].name} to {pokemon_dict[pokemon1_number]['name']} " # mal la parte de  {pokemon_dict[pokemon1_number]['name'], esto no esnecesariamente  el pokemon que debe ser 
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))

                #POKEMON AMIGO
                texto = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]['name']
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]['name']
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
               

                
            elif turn['second'][1] == 'atack':
                time.sleep(2)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if turn['second'][0] == best_team: 
                    pokemon1 = turn['second'][4] #current pokemon at that time  
                    pokemon1_number = int(pokedex_dict[pokemon1.name]) # pokemon podex number
                    pokemon2 = turn['first'][4]
                    pokemon2_number = int(pokedex_dict[pokemon2.name])
                else: 
                    pokemon2 = turn['second'][4] #current pokemon at that time  
                    pokemon2_number = int(pokedex_dict[pokemon2.name]) # pokemon podex number
                    pokemon1 = turn['first'][4]
                    pokemon1_number = int(pokedex_dict[pokemon1.name])
                imprimir(screen,pokemon1_number,pokemon2_number)
            
                #POKEMON AMIGO
                texto = pokemon_dict[int(pokedex_dict[turn['second'][3][0]])]['name']
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon_dict[int(pokedex_dict[turn['first'][3][0]])]['name']
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
               
                #textp de accion 
                text=  turn['second'][5]
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))
                pygame.display.update()

                if turn["first"][6]: 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    text=  f"{pokemon2.name} has fainted"#mismo q lo de arriba , mal 
                    imprimir(screen,pokemon1_number,pokemon2_number)
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

            
def pokemon_to_obj(poke_list: list, moves_dict, pokemon_dict, name: str, starter = 0) -> Team:
    dic = pokedex_number_dict()
    team_temp = []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team

def Pokemon_Enemigo(screen, texto_enemigo):
    rectangle = pygame.Rect(20, 90, 190, 20)     
    pygame.draw.rect(screen, (255,255,255), rectangle)
    text_width = texto_enemigo.get_width()
    text_height = texto_enemigo.get_height()
    screen.blit(texto_enemigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2)) 
    pygame.display.update()

def Pokemon_Amigo(screen, text_amigo):
    rectangle = pygame.Rect(457, 317, 195, 20) 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2))
    pygame.display.update()

def imprimir(screen,pokemon1_number,pokemon2_number): 
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1_number}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2_number}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))

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

    battel_log = simulated_fight(best_team,agus_team,effectiveness_dict,pokedex_dict,pokedex_dict,moves_dict)

    ganador = simulated_combat_gui(best_team,agus_team,effectiveness_dict,pokemon_dict,pokedex_dict,moves_dict,battel_log).pokemons
    
if __name__ == "__main__": 
    main()

























                

    #key: (Team, 'action', target, current_poke_stats, obj_poke_inicial, movimienot)
    # {'first': (<utils.team.Team object at 0x00000256A7F582F0>, 'switch', 2, ['Tyranitar', 200.0], <utils.pokemon.Pokemon object at 0x00000256A8210680>), 
    #  'second': (<utils.team.Team object at 0x00000256A8243560>, 'switch', 1, ['Delphox', 150.0], <utils.pokemon.Pokemon object at 0x00000256A8212C90>)},

                

               
        # while True:    
        #     next_turn = False
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         if event.type == pygame.KEYDOWN:
        #             screen.blit(background,[0, 0])
        #             next_turn = True
        #             break
        #     if next_turn:
        #         break
        #     pygame.display.flip()
            
        # pygame.quit()
        # sys.exit()

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
    