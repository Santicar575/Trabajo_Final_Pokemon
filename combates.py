from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
from graficos import get_best_team,pokedex_number_dict
from Algoritmo_genetico import leer_datos
import pygame, sys, time 

def simulated_fight(best_team, team2, effectiveness,pokemon_dict,pokedex_dict,moves_data):
    turn = 0    
    log_first, log_second = [], []

    while any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):            
        action_1, target_1 = best_team.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(best_team, effectiveness)
        fainted_1, fainted_2= None, None
        faint1, faint2 = 0, 0   
      
        # Switching always happens first
        if action_1 == 'switch': 
            first, second = best_team, team2
            poke1, poke2 = best_team.get_current_pokemon(), team2.get_current_pokemon()

        elif action_2 == 'switch':
            first, second = team2, best_team
            poke2, poke1 = best_team.get_current_pokemon(), team2.get_current_pokemon()
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
            
        # If nobody is switching, the fastest pokemon goes firsts
        elif best_team.get_current_pokemon().speed > team2.get_current_pokemon().speed: 
            first, second = best_team, team2
            poke1, poke2 = best_team.get_current_pokemon(), team2.get_current_pokemon()

        else:
            first, second = team2, best_team
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
            poke2, poke1 = best_team.get_current_pokemon(), team2.get_current_pokemon()
        
        movimeinto1 = first.return_action(action_1, target_1, second, effectiveness)
       
        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if first.get_current_pokemon().current_hp == 0 or second.get_current_pokemon().current_hp == 0:
            if first.get_current_pokemon().current_hp == 0:
                #print(f"{first.get_current_pokemon().name} has fainted")
                faint1 = 1 
                fainted_1,fainted_2 = __faint_change__(best_team, team2, effectiveness)
            else:
                #print(f"{second.get_current_pokemon().name} has fainted")
                faint2 = 1 
                fainted_2,fainted_1 = __faint_change__(best_team, team2, effectiveness)
    
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)
            movimeinto2 = second.return_action(action_2, target_2, first, effectiveness) 


            if first.get_current_pokemon().current_hp == 0 or second.get_current_pokemon().current_hp == 0:
                if first.get_current_pokemon().current_hp == 0:
                    faint1 = 1 
                    fainted_1, fainted_2  = __faint_change__(best_team, team2, effectiveness)
                    
                else:
                    #print(f"{second.get_current_pokemon().name} has fainted")
                    faint2 = 1
                    fainted_2, fainted_1 = __faint_change__(best_team, team2, effectiveness)

        log_first.append((turn, first.name, poke1.name,action_1, movimeinto1, first.get_current_pokemon().name, faint1, fainted_1))
        log_second.append((turn, second.name, poke2.name,action_2, movimeinto2, second.get_current_pokemon().name, faint2, fainted_2))
        turn += 1

    #Display who won
    winner = best_team if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else team2


    return log_first, log_second 

def simulated_combat_gui(best_team, team2, effectiveness,pokemon_dict,pokedex_dict,moves_data,log_first, log_second):
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
      
        for turn in range(len(log_first)):
            print(f"first: {log_first[turn]}")
            print(f"second: {log_second[turn]}")

           
#(0, 'Agus_team', 'Bouffalant', 'switch', 'Bouffalant switches to Delphox', 'Delphox', 0, None)
#(turn, team, pokemon inicial, accion, return accion, pokemon de salida, faint?, accion faint)
#///////////////////////////////////////////////////////////////////
            if log_first[turn][3]== "switch":
                time.sleep(1)
                screen.blit(background,[0,0]) #reseteo de fondo
                pygame.display.update()
              

                #cambio de imagenes
                if log_first[turn][1] == best_team.name: 
                    pokemon1_number = int(pokedex_dict[log_first[turn][5]])  #pokemon podex number
                    pokemon1 = log_first[turn][5]
                    pokemon2_number = int(pokedex_dict[log_second[turn][5]])
                    pokemon2 = log_second[turn][5]#current pokemon at that time as an object
                 
                  
                else: 
                    pokemon2_number = int(pokedex_dict[log_first[turn][5]]) # pokemon podex number
                    pokemon2 = log_first[turn][5]
                    pokemon1_number = int(pokedex_dict[log_second[turn][5]])
                    pokemon1 = log_second[turn][5]#current pokemon at that time as an object
              
                #POKEMON AMIGO
                texto = pokemon1
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO       
                texto = pokemon2
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)

                #texto de accion
                text = f"{log_first[turn][1]} change {log_first[turn][2]} to {log_first[turn][6]} "
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))

            elif log_first[turn][3] == "attack": 
                time.sleep(1)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if log_first[turn][1] == best_team.name: 
                    pokemon1 = log_first[turn][5] #current pokemon at that time  
                    pokemon1_number = int(pokedex_dict[pokemon1]) # pokemon podex number
                    pokemon2 = log_second[turn][5]
                    pokemon2_number = int(pokedex_dict[pokemon2])
                else: 
                    pokemon2 = log_first[turn][5] #current pokemon at that time  
                    pokemon2_number = int(pokedex_dict[pokemon2]) # pokemon podex number
                    pokemon1 = log_second[turn][5]
                    pokemon1_number = int(pokedex_dict[pokemon1])

                imprimir(screen,pokemon1_number,pokemon2_number)
            
                #POKEMON AMIGO
                texto = pokemon1
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon2
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
            
                #textp de accion 
                text=  log_first[turn][4]
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))
                pygame.display.update()

                if log_second[turn][6]: #si es true significa que el ataque derribo al enemigo
                    screen.blit(background,[0,0])
                    imprimir(screen, pokemon1_number, pokemon2_number)
                    text=  (f"{log_second[turn][5]} has fainted")
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

                    
                    screen.blit(background,[0,0])
                    imprimir(screen,pokemon1_number,pokemon2_number)
                    pokemon_change =  log_second[turn][5]
                    text = f"{pokemon1} has change to {pokemon_change}"
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()



                    if log_first[turn][7] == "switch":  # si el team que derribo al otro pokemon quiere cambiar
                        if log_first[turn][1] == best_team.name: 
                            pokemon2_number = int(pokedex_dict[log_second[turn][5]])  # pokemon podex number
                            pokemon1_number = int(pokedex_dict[log_first[turn][5]])
                        else:
                            pokemon1_number = int(pokedex_dict[log_second[turn][5]])  # pokemon podex number
                            pokemon2_number = int(pokedex_dict[log_first[turn][5]])
                        imprimir(screen, pokemon1_number, pokemon2_number)
                        pokemon_change =  log_first[turn][5]
                        text = f"{pokemon1} has change to {pokemon_change}"
                        pygame.draw.rect(screen, (255, 255, 255), rectangle)
                        text_surface = font.render(text, True, (0,0,0))
                        pygame.draw.rect(screen,(255,255,255),rectangle)
                        screen.blit(text_surface, (60, 470))
                        pygame.display.update()

#////////////////////////////////////////////////////////////////////
            elif log_first[turn][3] == 'skip': 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    text=  f"{log_first[turn][1]} has skip his turn"
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

#////////////////////////////////////////////////////////////////////
            if log_second[turn][3] == 'switch': 
                time.sleep(1)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if log_second[turn][1]== best_team.name: 
                    pokemon1_number = int(pokedex_dict[log_second[turn][5]])  # pokemon podex number
                    pokemon1 = log_second[turn][5]
                    pokemon2_number = int(pokedex_dict[log_first[turn][5]])
                    pokemon2 = log_first[turn][5] #current pokemon at that time as an object
                    
                else: 
                    pokemon1_number = int(pokedex_dict[log_first[turn][5]])  # pokemon podex number
                    pokemon1 = log_first[turn][5]
                    pokemon2_number = int(pokedex_dict[log_second[turn][5]])
                    pokemon2 = log_second[turn][5] #current pokemon at that time as an object
                imprimir(screen,pokemon1_number,pokemon2_number)                  

                #texto de accion
                text = f"{log_second[turn][1]} change {log_second[turn][2]} to {log_second[turn][5]} " 
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))

                #POKEMON AMIGO
                texto = pokemon1
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon2
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)

                pygame.display.update()

#////////////////////////////////////////////////////////////////////               
            elif log_second[turn][3] == 'atack':
                time.sleep(1)
                #reseteo de fondo
                screen.blit(background,[0,0])
                pygame.display.update()

                #cambio de imagenes
                if log_second[turn][1] == best_team.name: 
                    pokemon1 = log_second[turn][5] #current pokemon at that time  
                    pokemon1_number = int(pokedex_dict[pokemon1]) # pokemon podex number
                    pokemon2 = log_first[turn][5]
                    pokemon2_number = int(pokedex_dict[pokemon2])
                else: 
                    pokemon2 = log_second[turn][5] #current pokemon at that time  
                    pokemon2_number = int(pokedex_dict[pokemon2]) # pokemon podex number
                    pokemon1 = log_first[turn][5]
                    pokemon1_number = int(pokedex_dict[pokemon1])
                imprimir(screen,pokemon1_number,pokemon2_number)
            
                #POKEMON AMIGO
                texto = pokemon1
                texto_amigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)

                #POKEMON ENEMIGO         
                texto = pokemon2
                text_enemigo = font.render(texto, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
            
                #textp de accion 
                text=  log_second[turn][4]
                pygame.draw.rect(screen, (255, 255, 255), rectangle)
                text_surface = font.render(text, True, (0,0,0))
                pygame.draw.rect(screen,(255,255,255),rectangle)
                screen.blit(text_surface, (60, 470))
                pygame.display.update()

                if log_first[turn][6]: #si es true significa que el ataque derribo al enemigo
                    screen.blit(background,[0,0])
                    imprimir(screen,pokemon1_number,pokemon2_number)
                    text=  (f"{log_first[turn][5]} has fainted")
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()


                    screen.blit(background,[0,0])
                    imprimir(screen,pokemon1_number,pokemon2_number)
                    pokemon_change =  log_first[turn][5]
                    text = f"{pokemon1} has change to {pokemon_change}"
                    pygame.draw.rect(screen, (255, 255, 255), rectangle)
                    text_surface = font.render(text, True, (0,0,0))
                    pygame.draw.rect(screen,(255,255,255),rectangle)
                    screen.blit(text_surface, (60, 470))
                    pygame.display.update()

                    if log_second[turn][7] == "switch":  # si el team que derribo al otro pokemon qu
                        if log_second[turn][1] == best_team.name: 
                            pokemon2_number = int(pokedex_dict[log_second[turn][5]])  # pokemon podex number
                            pokemon1_number = int(pokedex_dict[log_first[turn][5]])
                        else:
                            pokemon1_number = int(pokedex_dict[log_second[turn][5]])  # pokemon podex number
                            pokemon2_number = int(pokedex_dict[log_first[turn][5]])
                        imprimir(screen, pokemon1_number, pokemon2_number)
                        pokemon_change =  log_second[turn][5]
                        text = f"{pokemon1} has change to {pokemon_change}"
                        pygame.draw.rect(screen, (255, 255, 255), rectangle)
                        text_surface = font.render(text, True, (0,0,0))
                        pygame.draw.rect(screen,(255,255,255),rectangle)
                        screen.blit(text_surface, (60, 470))
                        pygame.display.update()

        break
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
    

def Pokemon_Amigo(screen, text_amigo):
    rectangle = pygame.Rect(457, 317, 195, 20) 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2))
   

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

    log_first, log_second = simulated_fight(best_team,agus_team,effectiveness_dict,pokedex_dict,pokedex_dict,moves_dict)

    ganador = simulated_combat_gui(best_team,agus_team,effectiveness_dict,pokemon_dict,pokedex_dict,moves_dict,log_first,log_second).pokemons
    
if __name__ == "__main__": 
    main()

