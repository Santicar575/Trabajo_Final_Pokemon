from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
from graficos import get_best_team,pokedex_number_dict
from Algoritmo_genetico import leer_datos
import pygame, sys, time 
def simulated_fight(best_team, team2, effectiveness):
    turn = 0    
    log_first, log_second, hps = [], [], []
    while any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):            
        action_1, target_1 = best_team.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(best_team, effectiveness)
        fainted_1, fainted_2= None, None
        faint1, faint2 = 0, 0   
        movimeinto1, movimeinto2 = None, None
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
                faint1 = 1 
                fainted_1,fainted_2 = __faint_change__(best_team, team2, effectiveness)
            else:
                movimeinto2= f"{second.get_current_pokemon().name} has fainted"
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
                    movimeinto2= f"{second.get_current_pokemon().name} has fainted"
                    faint2 = 1
                    fainted_2, fainted_1 = __faint_change__(best_team, team2, effectiveness)
        hp_final_1 = best_team.get_current_pokemon().current_hp
        hp_final_2 = team2.get_current_pokemon().current_hp
        log_first.append((turn, first.name, poke1.name,action_1, movimeinto1, first.get_current_pokemon().name, faint1, fainted_1))
        log_second.append((turn, second.name, poke2.name,action_2, movimeinto2, second.get_current_pokemon().name, faint2, fainted_2))
        turn += 1
        hps.append((hp_final_1, hp_final_2))
    #Display who won
    winner = best_team if any(pokemon.current_hp > 0 for pokemon in best_team.pokemons) else team2
    return log_first, log_second, winner 

def simulated_combat_gui(best_team, pokemon_dict, pokedex_dict, log_first, log_second):
    # Create a new window
    pygame.init()
    
    # Set the size of the window
    screen = pygame.display.set_mode((772, 518))
    # Set the title of the window
    pygame.display.set_caption("Pokemon Battle")
    # Create a font object
    path = "Interfaz/pokemon_font.ttf"
    font = pygame.font.Font(path, 36)
    # #Create the backgroound for the window
    background = pygame.image.load("Interfaz/background.jpg").convert()
   
    screen.blit(background,[0,0])
    if log_first[0][1] == best_team.name:
        pokemon1_number = pokedex_dict[log_first[0][2]].zfill(3)
        pokemon2_number = pokedex_dict[log_second[0][2]].zfill(3)
    else:
        pokemon1_number = pokedex_dict[log_second[0][2]].zfill(3)
        pokemon2_number = pokedex_dict[log_first[0][2]].zfill(3)
        

    imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
    #LOG
    rectangle = pygame.Rect(30, 450, 680, 65) 
    text = "Inicio de batalla!!!"
    
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    # Dibujar el texto en la pantalla
    screen.blit(text_surface, (60, 470))

    #POKEMON AMIGO
    poke_amigo =pokemon_dict[int(pokemon1_number)]['name']
    texto_amigo = font.render(poke_amigo, True, (0, 0, 0))
    Pokemon_Amigo(screen, texto_amigo)
    
    #POKEMON ENEMIGO
    poke_enemigo = pokemon_dict[int(pokemon2_number)]['name']
    texto_enemigo = font.render(poke_enemigo, True, (0, 0, 0))
    Pokemon_Enemigo(screen, texto_enemigo)    
    imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
    pygame.display.update()
    turn, flag = 0, True
    while flag: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
      
            elif event.type == pygame.KEYDOWN:
                if turn >= len(log_first):
                    flag = False
                    break
#(0, 'Agus_team', 'Bouffalant', 'switch', 'Bouffalant switches to Delphox', 'Delphox', 0, None)
#(turn, team, pokemon inicial, accion, return accion, pokemon de salida, faint?, accion faint)
#///////////////////////////////////////////////////////////////////
                if log_first[turn][3]== "switch":
                  
                    screen.blit(background,[0,0]) #reseteo de fondo
                    pygame.display.update()
                
                    #cambio de imagenes
                    if log_first[turn][1] == best_team.name: 
                        pokemon1_inicio = log_first[turn][2] #current pokemon at the beginning
                        pokemon1_number = int(pokedex_dict[log_first[turn][5]])  #pokemon podex number
                        pokemon1 = log_first[turn][5]
                        pokemon2_inicio = log_second[turn][2]
                        pokemon2_number = int(pokedex_dict[log_second[turn][5]])
                        pokemon2 = log_second[turn][5]#current pokemon at that time as an object
                       
                    else: 
                        pokemon2_number = int(pokedex_dict[log_first[turn][5]]) # pokemon podex number
                        pokemon2 = log_first[turn][5]
                        pokemon1_number = int(pokedex_dict[log_second[turn][5]])
                        pokemon1 = log_second[turn][5]#current pokemon at that time as an object
                      
                    #POKEMON AMIGO
                    texto_amigo = font.render(pokemon1_inicio, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                    
                    #POKEMON ENEMIGO       
                    text_enemigo = font.render(pokemon2_inicio, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                    imprimir_pokemons(screen,pokedex_dict[pokemon1_inicio],pokedex_dict[pokemon2_inicio])
                
                    #texto de accion
                    text = f"{log_first[turn][1]} changes {log_first[turn][2]} to {log_first[turn][5]} "
                    texto_de_accion(screen,text,rectangle,font)
                    pygame.display.flip()
                    
                elif log_first[turn][3] == "attack": 
                    #reseteo de fondo
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
                
                    #POKEMON AMIGO
                    texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                    #POKEMON ENEMIGO       
                    text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                
                    #textp de accion 
                    text=  log_first[turn][4]
                    texto_de_accion(screen,text,rectangle,font)
                    pygame.display.update()
   
                    time.sleep(1)
                    if log_second[turn][6]: #si es true significa que el ataque derribo al enemigo
                        screen.blit(background,[0,0])
                        pygame.display.update()

                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
          
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                        imprimir_pokemons(screen, pokemon1_number, pokemon2_number)
                        text=  (f"{log_second[turn][2]} has fainted")
                        texto_de_accion(screen,text,rectangle,font)
                    
                        pygame.display.update()
                        time.sleep(1)
                       
                        screen.blit(background,[0,0])
                        pygame.display.update()
                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
                      
                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
     
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                        text = f"{log_second[turn][2]} has changed to {log_second[turn][5]}"
                        texto_de_accion(screen,text,rectangle,font)
                        pygame.display.update()
                        time.sleep(1)
                        if log_first[turn][7] == "switch":  # si el team que derribo al otro pokemon quiere cambiar
                            screen.blit(background,([0,0])) 
                            pygame.display.update()
                            imprimir_pokemons(screen, pokemon1_number, pokemon2_number)
                            
                            texto = pokemon1
                            texto_amigo = font.render(texto, True, (0, 0, 0))
                            Pokemon_Amigo(screen, texto_amigo)

                            texto = pokemon2
                            text_enemigo = font.render(texto, True, (0, 0, 0))
                            Pokemon_Enemigo(screen, text_enemigo)
                            text = f"{log_first[turn][2]} has changed to {log_first[turn][5]}"
                            texto_de_accion(screen,text,rectangle,font)
                            pygame.display.update()
                            
#////////////////////////////////////////////////////////////////////
                elif log_first[turn][3] == 'skip': 
                        screen.blit(background,[0,0])
                        pygame.display.update()
                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number)

                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
  
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)

                        text=  f"{log_first[turn][1]} has skipped his turn"
                        texto_de_accion(screen,text,rectangle,font)
                        pygame.display.update()

             
                time.sleep(1)
#////////////////////////////////////////////////////////////////////  CAMBIO DE LOG 
#////////////////////////////////////////////////////////////////////
                if log_second[turn][6]==0:
                    if log_second[turn][3] == 'switch':
                        #reseteo de fondo
                        screen.blit(background,[0,0])
                        pygame.display.update()
                  
                        if log_second[turn][1]== best_team.name: 
                            pokemon1_inicio= log_second[turn][2] #current pokemon at the beginning
                            pokemon2_inicio = log_first[turn][2]
                            pokemon1_number = pokedex_dict[pokemon1_inicio] # pokemon podex number
                            pokemon2_number = pokedex_dict[pokemon2_inicio]  
                        else: 
                            pokemon1_inicio= log_first[turn][2] #current pokemon at the beginning
                            pokemon2_inicio = log_second[turn][2]
                            pokemon1_number = pokedex_dict[pokemon1_inicio]  # pokemon podex number
                            pokemon2_number = pokedex_dict[pokemon2_inicio]

                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number)                  
                 
                        text = f"{log_second[turn][1]} changes {log_second[turn][2]} to {log_second[turn][5]} " 
                        texto_de_accion(screen,text,rectangle,font)
                
                        texto_amigo = font.render(pokemon1_inicio, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
                          
                        text_enemigo = font.render(pokemon2_inicio, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                        pygame.display.update()
        #////////////////////////////////////////////////////////////////////               
                    elif log_second[turn][3] == 'attack':
                       
                        screen.blit(background,[0,0])
                        pygame.display.update()
                        
                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
                    
                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
                             
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                
                        
                        text=  log_second[turn][4]
                        texto_de_accion(screen,text,rectangle,font)
                        #
                        pygame.display.update()
                        time.sleep(1)
                        ###############################################################################################
                        if log_first[turn][6]: #si es true significa que el ataque derribo al enemigo (Fainteo el pokemon de log_first)
                            screen.blit(background,[0,0])
                            pygame.display.update()
                            
                            texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                            Pokemon_Amigo(screen,texto_amigo)
                                  
                            text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                            Pokemon_Enemigo(screen, text_enemigo)
                            imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
                            text = (f"{log_first[turn][2]} has fainted")
                            texto_de_accion(screen,text,rectangle,font)

                            pygame.display.update() 
                            time.sleep(1)
                            screen.blit(background,[0,0])
                            pygame.display.update()
                            imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
                            #POKEMON AMIGO
                            texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                            Pokemon_Amigo(screen,texto_amigo)
                            #POKEMON ENEMIGO       
                            text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                            Pokemon_Enemigo(screen, text_enemigo)
                            text = f"{log_first[turn][2]} has changed to {log_first[turn][5]}"
                            texto_de_accion(screen,text,rectangle,font)
                            pygame.display.update()
                            time.sleep(1)
                            if log_second[turn][7] == "switch":  # si el team que derribo al otro pokemon quiere cambiar
                                screen.blit(background,[0,0])
                                pygame.display.update()
                                imprimir_pokemons(screen, pokemon1_number, pokemon2_number)
                                
                                texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                                Pokemon_Amigo(screen,texto_amigo)
                                      
                                text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                                Pokemon_Enemigo(screen, text_enemigo)
                                text = f"{log_second[turn][2]} has changed to {log_second[turn][5]}"
                                texto_de_accion(screen,text,rectangle,font)
                                pygame.display.update()
                               
                turn += 1   
    
        
def hp_bar(screen, hps_turno, pokemon1, pokemon2, pokemon_dict, moves_data): #151 es el 100% despues el porcentaje de vida_restante/vida_total va a ser lo que imprimamos en la vida
    largo_total = 151
    pokemon1, pokemon2 = Pokemon.from_dict(pokemon1, pokemon_dict, moves_data), Pokemon.from_dict(pokemon2, pokemon_dict, moves_data)
    vida_restante_1, vida_restante_2 = hps_turno[0], hps_turno[1]
    vida_total_1, vida_total_2 = pokemon1.stats['hp'], pokemon2.stats['hp']
    porcentaje1, porcentaje2 = (vida_restante_1/vida_total_1), (vida_restante_2/vida_total_2)
    largo1, largo2 = int(porcentaje1 * largo_total), int(porcentaje2 * largo_total)
    pass

def pokemon_to_obj(poke_list: list, moves_dict, pokemon_dict, name: str, starter = 0) -> Team:
    dic = pokedex_number_dict()
    team_temp = []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team

def texto_de_accion(screen,text,rectangle, font): 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    screen.blit(text_surface, (45, 470))
    pass 

def Pokemon_Enemigo(screen, texto_enemigo):
    rectangle = pygame.Rect(20, 85, 190, 20)     
    pygame.draw.rect(screen, (255,255,255), rectangle)
    text_width = texto_enemigo.get_width()
    text_height = texto_enemigo.get_height()
    screen.blit(texto_enemigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2)) 
    rect = pygame.Rect(151, 125, 150, 9)
    pygame.draw.rect(screen, (0, 255, 0), rect, border_radius = 5)

def Pokemon_Amigo(screen, text_amigo):
    rectangle = pygame.Rect(457, 317, 195, 20) 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2))
    rect = pygame.Rect(595, 353, 150, 9)
    pygame.draw.rect(screen, (0, 255, 0), rect, border_radius = 5)
   
def imprimir_pokemons(screen,pokemon1_number,pokemon2_number): 
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
    #Nuestro equipo es: Noivern, Turtonator, Aerodactyl, Tyranitar, Omastar, Pinsir
    elite_1 = pokemon_to_obj(pokemon_elite_1, moves_dict, pokemon_dict, "elite_1")
    elite_2 = pokemon_to_obj(pokemon_elite_2, moves_dict, pokemon_dict, "elite_2")
    elite_3 = pokemon_to_obj(pokemon_elite_3, moves_dict, pokemon_dict, "elite_3")
    elite_4 = pokemon_to_obj(pokemon_elite_4, moves_dict, pokemon_dict, "elite_4")
    champion = pokemon_to_obj(pokemon_champion, moves_dict, pokemon_dict, "champion")
    agus_team = pokemon_to_obj(agus_team, moves_dict, pokemon_dict, "Agus_team",0)
    log_first, log_second, winner = simulated_fight(best_team,agus_team,effectiveness_dict)
    #log_first, log_second = completar_logs()
    ganador = simulated_combat_gui(best_team, pokemon_dict, pokedex_dict, log_first, log_second).pokemons
    
if __name__ == "__main__": 
    main()