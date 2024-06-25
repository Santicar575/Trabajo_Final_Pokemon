import pygame.locals, pygame, sys, time
from utils.team import * 
from utils.pokemon import *
from funciones import *

def simulate_battle(team1: Team, team2: Team, effectiveness: dict, flag: bool) -> Team:
    """
    Simula una batalla entre dos equipos de pokemons
    
    Parameters:
    - team1: Equipo 1
    - team2: Equipo 2
    - effectiveness: Diccionario de efectividad

    return:
    - team1 o team2: Equipo ganador
    """

    pygame.mixer.music.stop()
    pygame.init()
    font, screen = pygame.font.Font("Interfaz/pokemon_font.ttf", 36), pygame.display.set_mode((772, 518))
    pygame.display.set_caption("Pokemon Battle")

    background = pygame.image.load("Interfaz/background.jpg")
    screen.blit(background, (0, 0))   
    pygame.mixer.music.load("Sonidos/Batalla.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2) 
    pygame.display.flip()
    pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()
    print_pokemons(screen, pokemon1.name, pokemon2.name, team1,team2)
    hp_bar(screen, pokemon1, pokemon2)

    if flag:
        wait_next_action()

    rectangle = pygame.Rect(30, 450, 680, 65) 
    text = "Inicio de batalla!!!"
    
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    screen.blit(text_surface, (60, 470))

    texto_amigo, texto_enemigo = team1.get_current_pokemon().name, team2.get_current_pokemon().name
    texto_amigo, texto_enemigo = font.render(texto_amigo, True, (0,0,0)), font.render(texto_enemigo, True, (0,0,0))
    pokemon_enemy(screen, texto_enemigo)
    pokemon_friend(screen, texto_amigo)
    pygame.display.flip()

    wait_next_action()

    turn = 0
    while any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
                
        print_pokemons(screen, team1.get_current_pokemon().name, team2.get_current_pokemon().name, team1, team2)
        hp_bar(screen, team1.get_current_pokemon(), team2.get_current_pokemon())
        texto_amigo, texto_enemigo = team1.get_current_pokemon().name, team2.get_current_pokemon().name
        pokemon_friend(screen, font.render(team1.get_current_pokemon().name, True, (0,0,0)))
        pokemon_enemy(screen, font.render(team2.get_current_pokemon().name, True, (0,0,0)))

        pygame.display.flip()

        action_1, target_1 = team1.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(team1, effectiveness)
        pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()

        # Switching always happens first
        if action_1 == 'switch':
            first, second = team1, team2
        elif action_2 == 'switch':
            first, second = team2, team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
        # If nobody is switching, the fastest pokemon goes firsts

        elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
            first, second = team1, team2
        else:
            first, second = team2, team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1

        action_1 = first.return_action(action_1, target_1, second, effectiveness)
        pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()
        print_action(screen, action_1, font, pokemon1.name, pokemon2.name, background, team1, team2) 
        hp_bar(screen, pokemon1, pokemon2)
        pygame.display.flip()
        wait_next_action() 
        
        # If any of the pokemons fainted, the turn ends, and both have the chance to switch
        if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()
            
            faint = team1 if team1.get_current_pokemon().current_hp == 0 else team2
            text = f"{faint.get_current_pokemon().name} fainted!!"
            text_surface = font.render(text, True, (0,0,0))
            print_action(screen, text, font, pokemon1.name, pokemon2.name, background, team1, team2)
            hp_bar(screen, pokemon1, pokemon2)
            pygame.display.flip()  
            wait_next_action()
            __faint_change__(team1, team2, effectiveness, font, pokemon1, pokemon2, screen, background)

        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)
            action_2 = second.return_action(action_2, target_2, first, effectiveness)
            pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()
            print_action(screen, action_2, font, pokemon1.name, pokemon2.name, background, team1, team2)
            hp_bar(screen, pokemon1, pokemon2)
            pygame.display.flip()   
            wait_next_action()                

            if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()
                
                faint = team1 if team1.get_current_pokemon().current_hp == 0 else team2
                text = f"{faint.get_current_pokemon().name} fainted!!"
                text_surface = font.render(text, True, (0,0,0))
                print_action(screen, text, font, pokemon1.name, pokemon2.name, background, team1, team2)
                hp_bar(screen, pokemon1, pokemon2)
                pygame.display.flip()  
                wait_next_action()
                __faint_change__(team1, team2, effectiveness, font, pokemon1.name, pokemon2.name, screen, background)

        turn += 1
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Sonidos/Victoria.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2) 
    print_action(screen, "The battle has ended", font, pokemon1.name, pokemon2.name, background, team1, team2)
    wait_next_action()
    if any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
        print_action(screen, "You won the battle", font, pokemon1.name, pokemon2.name, background, team1, team2)
    else: 
        print_action(screen, "You lost the battle", font, pokemon1.name, pokemon2.name, background, team1, team2)
    wait_next_action()
    pygame.quit()

def print_action(screen: pygame.Surface, accion: str, font: pygame.font.Font, pokemon1: Pokemon, pokemon2: Pokemon, background: pygame.image, team1: Team, team2: Team) -> None:
    """
    Imprime la accion en pantalla

    Parameters:
    - screen: Superficie de pygame
    - accion: Accion a imprimir
    - font: Fuente del texto
    - pokemon1: Pokemon 1
    - pokemon2: Pokemon 2
    - background: Imagen de fondo
    - team1: Equipo 1
    - team2: Equipo 2

    return:
    - None
    """

    screen.blit(background, (0,0))
    print_pokemons(screen, pokemon1, pokemon2, team1, team2)
    pokemon_friend(screen, font.render(pokemon1, True, (0,0,0)))
    pokemon_enemy(screen, font.render(pokemon2, True, (0,0,0)))
    action_text(screen, accion, pygame.Rect(30, 450, 680, 65), font)

def __faint_change__(team1: Team, team2: Team, effectiveness: dict, font: pygame.font.Font, pokemon1: Pokemon, pokemon2: Pokemon, screen: pygame.Surface, background: pygame.image) -> None:
    """"
    Cambio de pokemon cuando uno de los pokemons se desmaya
    
    Parameters:
    - team1: Equipo 1
    - team2: Equipo 2
    - effectiveness: Diccionario de efectividad
    - font: Fuente del texto
    - pokemon1: Pokemon 1
    - pokemon2: Pokemon 2
    - screen: Superficie de pygame
    - background: Imagen de fondo

    return:
    - None
    """
    if team1.get_current_pokemon().current_hp == 0:
        fainted_team, other_team = team1, team2
    else:
        fainted_team, other_team = team2, team1
    action_1, target_1 = fainted_team.get_next_action(other_team, effectiveness)
    action_1 = fainted_team.return_action(action_1, target_1, other_team, effectiveness)
    action_2, target_2 = other_team.get_next_action(fainted_team, effectiveness)
    pokemon1, pokemon2 = team1.get_current_pokemon(), team2.get_current_pokemon()

  
    hp_bar(screen, pokemon1, pokemon2)
    print_action(screen, action_1, font, pokemon1.name, pokemon2.name, background, team1, team2)
    wait_next_action()
    if action_2 == 'switch':
        action_2 = other_team.return_action(action_2, target_2, fainted_team, effectiveness)
        hp_bar(screen, pokemon1, pokemon2)
        print_action(screen, action_2, font, pokemon1.name, pokemon2.name, background, team1, team2)
        wait_next_action()
      
def wait_next_action() -> None:
    """"
    Espera a que el usuario presione una tecla para continuar
    
    return:
    - None"""
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

def hp_bar(screen: pygame.Surface, pokemon1: Pokemon, pokemon2: Pokemon) -> None: 
    """"
    Imprime la barra de vida de los pokemons en pantalla
    
    Parameters:
    - screen: Superficie de pygame
    - pokemon1: Pokemon del equipo 1
    - pokemon2: Pokemon del equipo 2
    - background: Imagen de fondo
    
    return:
    - None
    """
    
    #151 es el 100% despues el porcentaje de vida_restante/vida_total va a ser lo que imprimamos en la vida
    largo_total = 151
    vida_total_1, vida_total_2 =  pokemon1.max_hp, pokemon2.max_hp
    vida_restante_1, vida_restante_2 = pokemon1.current_hp, pokemon2.current_hp
    porcentaje1, porcentaje2 = (vida_restante_1/vida_total_1), (vida_restante_2/vida_total_2)

    largo1, largo2 = int(porcentaje1 * largo_total), int(porcentaje2 * largo_total)
    
    if porcentaje1 >= 0.5: color1 = (0, 255, 0)
    elif porcentaje1 >= 0.2: color1 = (255, 255, 0)
    else: color1 = (255, 0, 0)
     
    if porcentaje2 >= 0.5: color2 = (0, 255, 0)
    elif porcentaje2 >= 0.2: color2 = (255, 255, 0)
    else: color2 = (255, 0, 0)
    rect2, rect1 = pygame.Rect(151, 125, largo2, 9), pygame.Rect(595, 353, largo1, 9)
    pygame.draw.rect(screen, color1, rect1, border_radius = 5)
    pygame.draw.rect(screen, color2, rect2, border_radius = 5)

def menu(elite_1: Team, elite_2: Team, elite_3: Team, elite_4: Team, champion: Team, agus: Team, screen: pygame.Surface, title_font: pygame.font.Font, team_font: pygame.font.Font, font: pygame.font.Font, background_inicio: pygame.image, pokedex_dict: dict, screen_size: tuple, user_team: Team) -> tuple: 
    """
    Imprime el menu de seleccion de entrenadores en pantalla
    
    Parameters:
    - elite_1: Equipo del entrenador 1
    - elite_2: Equipo del entrenador 2
    - elite_3: Equipo del entrenador 3
    - elite_4: Equipo del entrenador 4
    - champion: Equipo del campeon
    - agus: Equipo de agus
    - screen: Superficie de pygame
    - title_font: Fuente del titulo
    - team_font: Fuente del equipo
    - font: Fuente del texto
    - background_inicio: Imagen de inicio
    - pokedex_dict: Diccionario que mapea nombres de pokemons a numeros de la pokedex
    - screen_size: Tamaño de la pantalla
    - user_team: Equipo del usuario

    return:
    - team: Equipo de pokemons del usuario
    - bool: Un booleano
    """
    screen = pygame.display.set_mode((512, 384))
    pygame.display.set_caption("Pokemon Battle")
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
                if 0<= x <= 254 and 0 <= y <= 91: return elite_1, False #will 
                    
                elif 0<= x <= 254 and 91 <= y <= 194: return elite_2, False #bruno
                    
                elif 0 <= x <= 254 and 194 <= y <= 286: return elite_3, False #koga
                    
                elif 255 <= x <= 512 and 0 <= y <= 110: return elite_4, False #karen 
                    
                elif 255 <= x <= 512 and 110 <= y <= 208: return champion, False #lance
                    
                elif 255 <= x <= 512 and 208 <= y <= 303: return agus, False #agus
                
                elif 384 <= x <= 512 and 320 <= y <= 384: return insert_team(screen, title_font, team_font, font, background_inicio, pokedex_dict, screen_size, user_team), True #team manual

def insert_team(screen: pygame.Surface, title_font: pygame.font.Font, team_font: pygame.font.Font, font: pygame.font.Font, background_inicio: pygame.image, pokedex_dict: dict, screen_size: tuple, team: Team) -> Team:
    """"
    Permite al usuario ingresar su equipo de pokemons
    
    Parameters:
    - screen: Superficie de pygame
    - title_font: Fuente del titulo
    - team_font: Fuente del equipo
    - font: Fuente del texto
    - background_inicio: Imagen de inicio
    - pokedex_dict: Diccionario que mapea nombres de pokemons a numeros de la pokedex
    - screen_size: Tamaño de la pantalla
    
    Returns:
    - team: Equipo de pokemons del usuario
    """
    
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

def select_best_team_button(screen: pygame.Surface) -> None:
    """
    Imprime el boton de seleccionar mejor equipo en pantalla
    
    Parameters:
    - screen: Superficie de pygame

    return: 
    - None
    """
    background =pygame.image.load("Interfaz/Seleccionar_equipo.png").convert()
    screen.blit(background,[0,0])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 105 <= x <= 250  and 450<= y <= 475:
                    return False
                elif 445 <= x <= 685 and 450 <= y <= 475:
                    return True
                      
def enemy_images(screen: pygame.Surface) -> None:
    """
    Imprime las imagenes de los entrenadores en pantalla
    
    Parameters:
    - screen: Superficie de pygame
    
    return:
    - None
    """
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
    """
    Convierte una lista de nombres de pokemons a objetos de la clase Pokemon

    Parameters:
    - poke_list: Lista de nombres de pokemons
    - moves_dict: Diccionario de movimientos
    - pokemon_dict: Diccionario de pokemons
    - name: Nombre del equipo
    - starter: Pokemon inicial

    return:
    - best_team: Equipo de pokemons
    """
    dic, team_temp = pokedex_number_dict(), []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team

def action_text(screen: pygame.Surface, text: pygame.font.Font, rectangle: pygame.Rect, font: pygame.font.Font) -> None: 
    """
    Impresion del texto de la accion en pantalla

    Parameters:
    - screen: Superficie de pygame
    - text: Texto de la accion
    - rectangle: Rectangulo donde se imprime el texto
    - font: Fuente del texto

    return:
    - None
    """    
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_surface = font.render(text, True, (0,0,0))
    pygame.draw.rect(screen,(255,255,255),rectangle)
    screen.blit(text_surface, (45, 470))
    pass 

def pokemon_enemy(screen: pygame.Surface, texto_enemigo: pygame.font.Font) -> None:
    """
    Impresion del nombre del pokemon enemigo en pantalla

    Parameters:
    - screen: Superficie de pygame
    - texto_enemigo: Nombre del pokemon enemigo
    
    return:
    - None
    """
    rectangle = pygame.Rect(20, 85, 190, 20)     
    pygame.draw.rect(screen, (255,255,255), rectangle)
    text_width = texto_enemigo.get_width()
    text_height = texto_enemigo.get_height()
    screen.blit(texto_enemigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2)) 
    
def pokemon_friend(screen: pygame.Surface, text_amigo: pygame.font.Font) -> None:
    """
    Impresion del nombre del pokemon amigo en pantalla

    Parameters:
    - screen: Superficie de pygame
    - text_amigo: Nombre del pokemon amigo
    
    return:
    - None
    """
    rectangle = pygame.Rect(457, 317, 195, 20) 
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    text_width = text_amigo.get_width()
    text_height = text_amigo.get_height()
    screen.blit(text_amigo, (rectangle.x + rectangle.width - text_width, rectangle.y + (rectangle.height - text_height) // 2))
     
def print_pokemons(screen: pygame.Surface, pokemon1: Pokemon, pokemon2: Pokemon, team1: Team, team2: Team, pokedex_dict = pokedex_number_dict()) -> None: 
    """"
    Imprime las imagenes de los pokemons en pantalla

    Parameters:
    - screen: Superficie de pygame
    - pokemon1: Pokemon del equipo 1
    - pokemon2: Pokemon del equipo 2
    - team1: Equipo 1
    - team2: Equipo 2
    - pokedex_dict: Diccionario que mapea nombres de pokemons a numeros de la pokedex

    Returns:
    - None
    """
    pokemon1_number, pokemon2_number = pokedex_dict[pokemon1].zfill(3), pokedex_dict[pokemon2].zfill(3)
    pokeball_image = pygame.transform.scale(pygame.image.load(f'Interfaz/pokemon_logo2.ico'),(20,20))
    x_amigo, x_enemigo = 450, 10
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1_number}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2_number}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))

    life_pokeball = pygame.transform.scale(pygame.image.load("Interfaz/pokemon_logo.ico"),(20,20))
    death_pokeball = pygame.transform.scale(pygame.image.load("Interfaz/pokemon_logo2.ico"),(20,20))
    for pokemon in team1.pokemons:
        if pokemon.current_hp > 0: screen.blit(life_pokeball, (x_amigo, 270))
        else: screen.blit(death_pokeball, (x_amigo, 270))
        x_amigo += 20
    for pokemon in team2.pokemons:
        if pokemon.current_hp > 0: screen.blit(life_pokeball, (x_enemigo, 40))
        else: screen.blit(death_pokeball, (x_enemigo, 40))
        x_enemigo += 20
    
def main():
    moves_dict, pokemon_dict, effectiveness_dict = leer_datos()
    pokedex_dict = pokedex_number_dict() 

    pokemon_elite_1 = ["Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"]
    pokemon_elite_2 = ["Skuntank", "Toxicroak", "Swalot", "Venomoth", "Muk", "Crobat"]
    pokemon_elite_3 = ["Hitmontop", "Hitmonlee", "Hariyama", "Machamp", "Lucario", "Hitmonchan"]
    pokemon_elite_4 = ["Weavile", "Spiritomb", "Honchkrow", "Umbreon", "Houndoom", "Absol"]
    pokemon_champion = ["Salamence", "Garchomp", "Dragonite", "Charizard", "Altaria", "Gyarados"]
    agus_team = ["Bouffalant","Delphox","Mamoswine","Tsareena","Greninja","Slaking"]
    team = get_best_team(50)

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
    font, title_font, team_font = pygame.font.Font(None, 36), pygame.font.Font(None, 72), pygame.font.Font(None, 50)

    # Create a list to store the user's team and the opponent's team
    user_team, opponent_team = [], []

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
    if select_best_team_button(screen) == True:
        user_team = team[4:]
    else:
        user_team = insert_team(screen, title_font, team_font, font, background_inicio, pokedex_dict, screen_size, user_team)
       
    user_team = insert_team(screen, title_font, team_font, font, background_inicio, pokedex_dict, screen_size, user_team)
    user_team = pokemon_to_obj(user_team, moves_dict, pokemon_dict, "user_team")

    opponent_team, flag = menu(pokemon_elite_1, pokemon_elite_2, pokemon_elite_3, pokemon_elite_4, pokemon_champion, agus_team, screen, title_font, team_font, font, background_inicio, pokedex_dict, screen_size, opponent_team)
    opponent_team = pokemon_to_obj(opponent_team, moves_dict, pokemon_dict, "opponent_team")
    simulate_battle(user_team, opponent_team, effectiveness_dict, flag)    

if __name__ == "__main__": 
    main()