import pygame.locals
from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
import pygame, sys, time 
from funciones import *


def simulated_fight(best_team: Team, team2: Team, effectiveness: dict) -> tuple:
    """
    Simula la pelea entre los dos equipos Pokémon seleccionados.

    Parámetros:
    - best_team (Team): Equipo de Pokémon del jugador principal.
    - team2 (Team): Equipo de Pokémon del oponente.
    - effectiveness (dict): Diccionario que contiene la efectividad de los movimientos de los Pokémon.

    Retorna:
    - log_first (list): Lista que contiene el registro de acciones del jugador principal.
    - log_second (list): Lista que contiene el registro de acciones del oponente.
    - hps (list): Lista que contiene los puntos de vida finales de los Pokémon al final de cada turno.
    - winner (Team): Equipo ganador de la pelea.
    """
    turn = 0    
    log_first, log_second, hps = [], [], {}
    
    for pokemon1, pokemon2 in zip(best_team.pokemons, team2.pokemons):
        hps[pokemon1.name] = [pokemon1.max_hp/2]
        hps[pokemon2.name] = [pokemon2.max_hp/2]

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
                movimeinto2= f"{second.get_current_pokemon().name} ha sido debilitado"
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
                    movimeinto2= f"{second.get_current_pokemon().name} ha sido debilitado"
                    faint2 = 1
                    fainted_2, fainted_1 = __faint_change__(best_team, team2, effectiveness)
        
        contador1, contador2 = 0, 0
        for pokemon1, pokemon2 in zip(best_team.pokemons, team2.pokemons):
            if pokemon1.current_hp != 0: contador1 +=1
            if pokemon2.current_hp != 0: contador2 +=1
            hps[pokemon1.name] += [pokemon1.current_hp/2]
            hps[pokemon2.name] += [pokemon2.current_hp/2]

        if first.name == best_team.name:
            log_first.append((turn, first.name, poke1.name,action_1, movimeinto1, first.get_current_pokemon().name, faint1, fainted_1, contador1))
            log_second.append((turn, second.name, poke2.name,action_2, movimeinto2, second.get_current_pokemon().name, faint2, fainted_2, contador2))
        else:
            log_first.append((turn, first.name, poke1.name,action_1, movimeinto1, first.get_current_pokemon().name, faint1, fainted_1, contador2))
            log_second.append((turn, second.name, poke2.name,action_2, movimeinto2, second.get_current_pokemon().name, faint2, fainted_2, contador1))
        turn += 1

    for i in range(len(log_first)):
        print(log_first[i])
        print(log_second[i])
    return log_first, log_second, hps


def simulated_combat_gui(best_team: Team, pokemon_dict: dict, pokedex_dict: dict, log_first: list, log_second: list, hps: list) -> None:
    """
    Grafica la pelea de Pokémon en una interfaz gráfica.

    Parámetros:
    - best_team (Team): El equipo de Pokémon del jugador.
    - pokemon_dict (dict): Un diccionario que contiene información sobre los Pokémon.
    - pokedex_dict (dict): Un diccionario que mapea los nombres de los Pokémon a sus números en la Pokédex.
    - log_first (list): Una lista que registra las acciones del primer jugador.
    - log_second (list): Una lista que registra las acciones del segundo jugador.
    - hps (list): Una lista que contiene los puntos de vida actuales de los Pokémon.

    Retorna:
    None
    """
    pygame.mixer.music.stop()
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

    pygame.mixer.music.load("Sonidos/Batalla.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2) 
   
    screen.blit(background,[0,0])
    if log_first[0][1] == best_team.name:
        pokemon1_number = pokedex_dict[log_first[0][2]].zfill(3)
        pokemon2_number = pokedex_dict[log_second[0][2]].zfill(3)
        contador1, contador2 = log_first[0][8], log_second[0][8]
    else:
        pokemon1_number = pokedex_dict[log_second[0][2]].zfill(3)
        pokemon2_number = pokedex_dict[log_first[0][2]].zfill(3)
        contador1, contador2 = log_second[0][8], log_first[0][8]
        
    # imprimir_pokemons(screen,pokemon1_number,pokemon2_number)
    # print(hps)
    # print("/////")
    rectangle = pygame.Rect(30, 450, 680, 65) 
    text = "Inicio de batalla!!!"
    
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    screen.blit(text_surface, (60, 470))
    
    poke_amigo =pokemon_dict[int(pokemon1_number)]['name']
    texto_amigo = font.render(poke_amigo, True, (0, 0, 0))
    Pokemon_Amigo(screen, texto_amigo)
    
    poke_enemigo = pokemon_dict[int(pokemon2_number)]['name']
    texto_enemigo = font.render(poke_enemigo, True, (0, 0, 0))
    Pokemon_Enemigo(screen, texto_enemigo)    
    imprimir_pokemons(screen,pokemon1_number,pokemon2_number,0,hps,pokemon_dict,pokedex_dict,contador1, contador2)
    pygame.display.update()
    turn = 0
    flag = True
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()               
#(0, 'Agus_team', 'Bouffalant', 'switch', 'Bouffalant switches to Delphox', 'Delphox', 0, None)
#(turn, team, pokemon inicial, accion, return accion, pokemon de salida, faint?, accion faint)
#///////////////////////////////////////////////////////////////////
            if log_first[turn][3]== "switch":
                
                screen.blit(background,[0,0]) 
                pygame.display.update()
            
                if log_first[turn][1] == best_team.name: 
                    pokemon1_inicio = log_first[turn][2]
                    pokemon1_number = int(pokedex_dict[log_first[turn][5]].zfill(3))

                    pokemon2_inicio = log_second[turn][2]
                    pokemon2_number = int(pokedex_dict[log_second[turn][5]].zfill(3))
                    contador1, contador2 = log_first[turn][8], log_second[turn][8]
                else: 
                    pokemon2_number = int(pokedex_dict[log_first[turn][5]].zfill(3))
                    pokemon2_inicio = log_first[turn][2]
                    pokemon1_number = int(pokedex_dict[log_second[turn][5]].zfill(3))
                    pokemon1_inicio = log_second[turn][2]
                    contador1, contador2 = log_second[turn][8], log_first[turn][8]                        
                    
                texto_amigo = font.render(pokemon1_inicio, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)
                
                text_enemigo = font.render(pokemon2_inicio, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
                text = f"{log_first[turn][1]} changes {log_first[turn][2]} to {log_first[turn][5]} "
                texto_de_accion(screen,text,rectangle,font)
                imprimir_pokemons(screen,pokedex_dict[pokemon1_inicio].zfill(3),pokedex_dict[pokemon2_inicio].zfill(3),turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                pygame.display.flip()
                
            elif log_first[turn][3] == "attack": 
                screen.blit(background,[0,0])
                pygame.display.update()
                if log_first[turn][1] == best_team.name:
                    pokemon1 = log_first[turn][2]
                    pokemon1_number = pokedex_dict[pokemon1].zfill(3)
                    pokemon2 = log_second[turn][2]
                    pokemon2_number = pokedex_dict[pokemon2].zfill(3)
                    contador1, contador2 = log_first[turn][8], log_second[turn][8]
                else:
                    pokemon2 = log_first[turn][2]
                    pokemon2_number = pokedex_dict[pokemon2].zfill(3)
                    pokemon1 = log_second[turn][2]
                    pokemon1_number = pokedex_dict[pokemon1].zfill(3)
                    contador1, contador2 = log_second[turn][8], log_first[turn][8]
            
                texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                Pokemon_Amigo(screen,texto_amigo)
                        
                text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                Pokemon_Enemigo(screen, text_enemigo)
            
                text=  log_first[turn][4]
                texto_de_accion(screen,text,rectangle,font)
                imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                pygame.display.update()
                wait_next_acton()

                if log_second[turn][6]: 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    
                    texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                            
                    text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                    text=  (f"{log_second[turn][2]} has fainted")
                    texto_de_accion(screen,text,rectangle,font)
                    imprimir_pokemons(screen, pokemon1_number, pokemon2_number,turn,hps,pokemon_dict,pokedex_dict, contador1, contador2)

                    pygame.display.update()
                    wait_next_acton()
        
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    
                    texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                            
                    text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                    imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                    if turn != len(log_first)-1:
                        text = f"{log_second[turn][2]} has changed to {log_second[turn][5]}"
                        texto_de_accion(screen,text,rectangle,font)
                        pygame.display.update()
                        wait_next_acton()
                        if log_first[turn][7] == "switch": 
                            screen.blit(background,([0,0])) 
                            pygame.display.update()
                            
                            texto = pokemon1
                            texto_amigo = font.render(texto, True, (0, 0, 0))
                            Pokemon_Amigo(screen, texto_amigo)
                            texto = pokemon2
                            text_enemigo = font.render(texto, True, (0, 0, 0))
                            Pokemon_Enemigo(screen, text_enemigo)
                            text = f"{log_first[turn][2]} has changed to {log_first[turn][5]}"
                            texto_de_accion(screen,text,rectangle,font)
                            imprimir_pokemons(screen, pokemon1_number, pokemon2_number,turn,hps,pokemon_dict,pokedex_dict, contador1, contador2)

                            pygame.display.update()
                    else:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("Sonidos/Victoria.mp3")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.2) 
                        text = f"{log_first[turn][1].upper()} IS THE WINNER"
                        texto_de_accion(screen,text,rectangle,font)
                        pygame.display.update()
                        time.sleep(5)
                        return 


            elif log_first[turn][3] == 'skip': 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    
                    texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                            
                    text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                    
                    text=  f"{log_first[turn][1]} has skipped his turn"
                    texto_de_accion(screen,text,rectangle,font)
                    imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)
                    
                    pygame.display.update()
            wait_next_acton()
#////////////////////////////////////////////////////////////////////  CAMBIO DE LOG 
#////////////////////////////////////////////////////////////////////
            if log_second[turn][6]==0:
                if log_second[turn][3] == 'switch': 
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    if log_second[turn][1]== best_team.name: 
                        pokemon1_inicio= log_second[turn][2] 
                        pokemon2_inicio = log_first[turn][2]
                        pokemon1_number = pokedex_dict[pokemon1_inicio].zfill(3)
                        pokemon2_number = pokedex_dict[pokemon2_inicio].zfill(3)
                        contador1, contador2 = log_second[turn][8], log_first[turn][8] 
                    else: 
                        pokemon1_inicio= log_first[turn][2] 
                        pokemon2_inicio = log_second[turn][2]
                        pokemon1_number = pokedex_dict[pokemon1_inicio].zfill(3) 
                        pokemon2_number = pokedex_dict[pokemon2_inicio].zfill(3)
                        contador1, contador2 = log_first[turn][8], log_second[turn][8]

                    text = f"{log_second[turn][1]} changes {log_second[turn][2]} to {log_second[turn][5]} " 
                    texto_de_accion(screen,text,rectangle,font)
            
                    texto_amigo = font.render(pokemon1_inicio, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                            
                    text_enemigo = font.render(pokemon2_inicio, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
                    imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1,contador2)   

                    pygame.display.update()
    #////////////////////////////////////////////////////////////////////               
                elif log_second[turn][3] == 'attack':
                    screen.blit(background,[0,0])
                    pygame.display.update()
                    
                    if log_second[turn][1] == best_team.name: 
                        pokemon1 = log_second[turn][2]   
                        pokemon1_number = pokedex_dict[pokemon1].zfill(3)
                        pokemon2 = log_first[turn][2]
                        pokemon2_number = pokedex_dict[pokemon2].zfill(3)
                        contador1, contador2 = log_second[turn][8], log_first[turn][8]
                    else: 
                        pokemon2 = log_second[turn][2] 
                        pokemon2_number = pokedex_dict[pokemon2].zfill(3)
                        pokemon1 = log_first[turn][2]
                        pokemon1_number = pokedex_dict[pokemon1].zfill(3)
                        contador1, contador2 = log_first[turn][8], log_second[turn][8]                    

            
                    texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                    Pokemon_Amigo(screen,texto_amigo)
                            
                    text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                    Pokemon_Enemigo(screen, text_enemigo)
        
                    text=  log_second[turn][4]
                    texto_de_accion(screen,text,rectangle,font)
                    imprimir_pokemons(screen, pokemon1_number, pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                    pygame.display.update()
                    wait_next_acton()
                    ###############################################################################################
                    if log_first[turn][6]: 
                        screen.blit(background,[0,0])
                        pygame.display.update()
                        
                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
                                
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                        text = (f"{log_first[turn][2]} has fainted")
                        texto_de_accion(screen,text,rectangle,font)
                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                        pygame.display.update() 
                        wait_next_acton()
                        screen.blit(background,[0,0])
                        pygame.display.update()
                        texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                        Pokemon_Amigo(screen,texto_amigo)
                        text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                        Pokemon_Enemigo(screen, text_enemigo)
                        imprimir_pokemons(screen,pokemon1_number,pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                        if turn != len(log_first)-1:
                            text = f"{log_first[turn][2]} has changed to {log_first[turn][5]}"
                            texto_de_accion(screen,text,rectangle,font)
                            pygame.display.update()
                            wait_next_acton()
                            if log_second[turn][7] == "switch":  
                                screen.blit(background,[0,0])
                                pygame.display.update()

                                texto_amigo = font.render(pokemon1, True, (0, 0, 0))
                                Pokemon_Amigo(screen,texto_amigo)
                                    
                                text_enemigo = font.render(pokemon2, True, (0, 0, 0))
                                Pokemon_Enemigo(screen, text_enemigo)
                                text = f"{log_second[turn][2]} has changed to {log_second[turn][5]}"
                                texto_de_accion(screen,text,rectangle,font)
                                imprimir_pokemons(screen, pokemon1_number, pokemon2_number,turn,hps,pokemon_dict,pokedex_dict,contador1, contador2)

                                pygame.display.update() 
                        else:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("Sonidos/Victoria.mp3")
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.2)  
                            text = f"{log_second[turn][1].upper()} IS THE WINNER"
                            texto_de_accion(screen,text,rectangle,font)
                            pygame.display.update()
                            time.sleep(5)
                            return
            turn += 1   


def wait_next_acton():
    while True:
        next_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                next_turn = True
                break
        if next_turn:
            break
        pygame.display.flip()


def hp_bar(screen: pygame.Surface, turno: int, hps: dict, pokemon1_number: int, pokemon2_number: int, pokemon_dict: dict, pokedex_dict: dict) -> None: #151 es el 100% despues el porcentaje de vida_restante/vida_total va a ser lo que imprimamos en la vida
    largo_total = 151
    #{'nombre': [vida0, vida1, vida2,....]}

    pokemon1, pokemon2 = pokemon_dict[int(pokemon1_number)]['name'], pokemon_dict[int(pokemon2_number)]['name']


    vida_restante_1, vida_restante_2 = hps[pokemon1][turno+1], hps[pokemon2][turno+1]
    

    vida_total_1, vida_total_2 = hps[pokemon1][0], hps[pokemon2][0]

    porcentaje1, porcentaje2 = (vida_restante_1/vida_total_1), (vida_restante_2/vida_total_2)

    largo1, largo2 = int(porcentaje1 * largo_total), int(porcentaje2 * largo_total)
    print(largo1, largo2)
    
    if porcentaje1 >= 0.5:
        color1 = (0, 255, 0)
    elif porcentaje1 >= 0.2:
        color1 = (255, 255, 0)
    else:
        color1 = (255, 0, 0)
     
    if porcentaje2 >= 0.5:
        color2 = (0, 255, 0)
    elif porcentaje2 >= 0.2:
        color2 = (255, 255, 0)
    else:
        color2 = (255, 0, 0)

    rect1 = pygame.Rect(151, 125, largo1, 9)
    rect2 = pygame.Rect(595, 353, largo2, 9)
    pygame.draw.rect(screen, color1, rect1, border_radius = 5)
    pygame.draw.rect(screen, color2, rect2, border_radius = 5)

def menu(elite_1,elite_2,elite_3,elite_4,champion, agus, screen, title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team): 
    pygame.init()
    screen = pygame.display.set_mode((512, 384))
    pygame.display.set_caption("Pokemon Battle")
    path = "Interfaz/pokemon_font.ttf"
    background = pygame.image.load("Interfaz/pokemon_menu.png").convert()
    screen.blit(background,[0,0])
    enemy_images(screen)
    pygame.display.update()
    while True:
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:   
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 0<= x <= 254 and 0 <= y <= 91: #will 
                    return elite_1
                    
                elif 0<= x <= 254 and 91 <= y <= 194:#bruno
                    return elite_3
                    
                elif 0 <= x <= 254 and 194 <= y <= 286: #koga
                    return elite_2
                    
                elif 255 <= x <= 512 and 0 <= y <= 110: #karen 
                    return elite_4
                    
                elif 255 <= x <= 512 and 110 <= y <= 208: #lance
                    return champion
                    
                elif 255 <= x <= 512 and 208 <= y <= 303:
                    return agus
                
                elif 384 <= x <= 512 and 320 <= y <= 384:
                    return ingresar_equipo(screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)

def ingresar_equipo(screen: pygame.Surface, title_font: pygame.font.Font, team_font: pygame.font.Font, font: pygame.font.Font, background_inicio, pokedex_dict: dict, screen_size: tuple, team: Team) -> Team:
    title = title_font.render('Enter your team', True, (0,0,0))
    screen = pygame.display.set_mode((772, 518))
    # Create a string to store the current input
    current_input = ''
    
    while True:
        # Calculate the position of the title
        title_pos = ((screen_size[0] - title.get_width()) // 2, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # When the user presses enter, add the current input to the user's team
                    current_input = current_input.lower().capitalize()
                    if current_input not in pokedex_dict:
                        screen.blit(background_inicio,[0,0])
                        text = font.render("That pokemon does not exist!!", True, (0,0,0))
                        screen.blit(text, (20, 20))
                        pygame.display.flip()
                        time.sleep(1)
                        current_input = ''
                    else:
                        if current_input in team:
                            screen.blit(background_inicio,[0,0])
                            text = font.render("You already have that pokemon in your team!!", True, (0,0,0))
                            screen.blit(text, (20, 20))
                            pygame.display.flip()
                            time.sleep(1)
                            current_input = ''
                        else:
                            team.append(current_input)
                            current_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    # When the user presses backspace, remove the last character from the current input
                    current_input = current_input[:-1]
                elif event.key == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if 350 <= x <= 400 and 0 <= y <= 50:
                        pass     
                else:
                    # When the user presses any other key, add it to the current input
                    current_input += event.unicode

        # Clear the screen
        screen.blit(background_inicio,[0,0])
        screen.blit(title, title_pos)
        # Draw the current input
        text = font.render(current_input, True, (0,0,0))
        screen.blit(text, (20, 80))

        # Draw the user's team
        team_text = team_font.render('Current team', True, (0,0,0))
        for i, pokemon in enumerate(team):
            screen.blit(team_text, (20, 120))
            # Calculate the position of the Pokemon image
            s = 3  # Number of columns
            x = 20 + (i % s) * (screen_size[0] // s)
            y = 160 + (i // s) * 160
            pokemon_image = pygame.image.load(f'data/imgs/{str(pokedex_dict[pokemon]).zfill(3)}.png')
            screen.blit(pokemon_image, (x, y))
        if len(team) == 6:
            pygame.display.flip()
            time.sleep(1)
            return team
        pygame.display.flip()


def select_best_team_button(screen, font, img_inicio):
    text1 = "Enter your team"
    text2 = "Select best team"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 425 <= x <= 425 + 200 and 250 <= y <= 250 + 100:
                    return True
                elif 425 <= x <= 425 + 200 and 250 <= y <= 250 + 100:
                    return False
                
        screen.blit(pygame.image.load("Interfaz/button.png"), (200,250))
        screen.blit(pygame.image.load("Interfaz/button.png"), (425,250))

        pygame.display.flip()
                
def enemy_images(screen: pygame.Surface) -> None:
    bruno = pygame.transform.scale(pygame.image.load(f'data/imgs/bruno.png'),(55,55))
    will  = pygame.transform.scale(pygame.image.load(f'data/imgs/will.png'),(67,67))
    koga = pygame.transform.scale(pygame.image.load(f'data/imgs/koga.png'),(70,70))
    karen = pygame.transform.scale(pygame.image.load(f'data/imgs/karen.png'),(67,67))
    lance = pygame.transform.scale(pygame.image.load(f'data/imgs/lance.png'),(70,70))
    agus = pygame.transform.scale(pygame.image.load(f'data/imgs/agus_character.png'),(65,65))

    screen.blit(will, (10, 1))
    screen.blit(bruno, (10, 100))
    screen.blit(koga, (10, 185))
    screen.blit(karen, (269, 10))
    screen.blit(lance ,(269, 105))
    screen.blit(agus, (269,205))
    pass

def pokemon_to_obj(poke_list: list, moves_dict: dict, pokemon_dict: dict, name: str, starter: int = 0) -> Team:
    dic = pokedex_number_dict()
    team_temp = []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team

def texto_de_accion(screen: pygame.Surface, text: pygame.font.Font, rectangle: pygame.Rect, font: pygame.font.Font) -> None: 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    screen.blit(text_surface, (45, 470))
    pass 

def Pokemon_Enemigo(screen: pygame.Surface, texto_enemigo: pygame.font.Font) -> None:
    rectangle = pygame.Rect(20, 85, 190, 20)     
    pygame.draw.rect(screen, (255,255,255), rectangle)
    text_width = texto_enemigo.get_width()
    text_height = texto_enemigo.get_height()
    screen.blit(texto_enemigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2)) 
    rect = pygame.Rect(151, 125, 150, 9)
    pygame.draw.rect(screen, (0, 255, 0), rect, border_radius = 5)

def Pokemon_Amigo(screen: pygame.Surface, text_amigo: pygame.font.Font) -> None:
    rectangle = pygame.Rect(457, 317, 195, 20) 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2))
    rect = pygame.Rect(595, 353, 150, 9)
    pygame.draw.rect(screen, (0, 255, 0), rect, border_radius = 5)
   
def pokeball_viva(screen, amigo: bool, x: int):
    pokeball_image = pygame.transform.scale(pygame.image.load(f'Interfaz/pokemon_logo.ico'),(20,20))
    if amigo:
        screen.blit(pokeball_image, (x, 270))
    else:
        screen.blit(pokeball_image, (x, 40))
    

def imprimir_pokemons(screen: pygame.Surface, pokemon1_number: int, pokemon2_number: int,turno:int, hps:dict, pokemon_dict:int, pokedex_dict:dict, contador1: int, contador2: int ) -> None: 
    pokeball_image = pygame.transform.scale(pygame.image.load(f'Interfaz/pokemon_logo2.ico'),(20,20))
    x_amigo, x_enemigo = 450, 10
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1_number}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2_number}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))
    hp_bar(screen, turno, hps, pokemon1_number, pokemon2_number, pokemon_dict, pokedex_dict) 
    
    for i in range(6):
        screen.blit(pokeball_image, (x_enemigo, 40))
        x_enemigo += 20

    for i in range(6):
        screen.blit(pokeball_image, (x_amigo, 270))
        x_amigo += 20

    x_amigo, x_enemigo = 450, 10
    for i in range(contador1):
        pokeball_viva(screen, True, x_amigo)
        x_amigo += 20
    
    for i in range(contador2):
        pokeball_viva(screen, False, x_enemigo)
        x_enemigo += 20

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

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Set the size of the window
    screen = pygame.display.set_mode((514, 389))

    # Set the title of the window
    pygame.display.set_caption("Pokemon Battle")
    pygame.mixer.music.load("Sonidos/Inicio.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2) 

    # Create a font object
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 72)
    team_font = pygame.font.Font(None, 50)

    # Create a list to store the user's team and the opponent's team
    user_team = ["Mewtwo", "Mew", "Rayquaza", "Arceus", "Giratina", "Dialga"]
    opponent_team = []
    
    inicio = True
    img_inicio = pygame.image.load("Interfaz/Img_inicio.png").convert()
    screen.blit(img_inicio,[0,0])
    pygame.display.update()
    while inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    inicio = False
    screen = pygame.display.set_mode((772, 518))
    background_inicio = pygame.image.load("Interfaz/background2.jpg").convert()
    screen_size = screen.get_size()
    background_inicio = pygame.transform.scale(background_inicio, screen_size)
    screen.blit(background_inicio,[0,0])
    pygame.display.flip()
    # Game loop
    # if select_best_team_button(screen, font, background_inicio) == True:
    #     user_team = best_team
    # else:
    #     user_team = ingresar_equipo(screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)

    user_team = ingresar_equipo(screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)
    user_team = pokemon_to_obj(user_team, moves_dict, pokemon_dict, "user_team")

    opponent_team = menu(elite_1, elite_2, elite_3, elite_4, champion, agus_team, screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)
    

    if opponent_team != []:
        log_first, log_second, hps = simulated_fight(user_team, opponent_team, effectiveness_dict)
        simulated_combat_gui(user_team, pokemon_dict, pokedex_dict, log_first, log_second, hps)
    
    # Update the display
    pygame.display.flip()

if __name__ == "__main__": 
    main()