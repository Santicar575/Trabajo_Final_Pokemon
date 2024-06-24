import pygame.locals
from utils.combat import __faint_change__
from utils.team import * 
from utils.pokemon import *
import pygame, sys, time 
from funciones import *

def simulate_battle(team1, team2, effectiveness,pokemon_dict, moves_dict) -> Team:

        pygame.mixer.music.stop()
        
        pygame.init()

        font = pygame.font.Font("Interfaz/pokemon_font.ttf", 36)

        screen = pygame.display.set_mode((772, 518))
        pygame.display.set_caption("Pokemon Battle")

        background = pygame.image.load("Interfaz/background.jpg")
        screen.blit(background, (0, 0))
        
        pygame.mixer.music.load("Sonidos/Batalla.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2) 
        pygame.display.flip()

        pokemon1 = team1.get_current_pokemon()
        pokemon2 = team2.get_current_pokemon()
        hp_bar(screen, pokemon1, pokemon2,background) 
        imprimir_pokemons(screen, pokemon1.name, pokemon2.name,team1,team2)
        

        rectangle = pygame.Rect(30, 450, 680, 65) 
        text = "Inicio de batalla!!!"
        
        text_surface = font.render(text, True, (0,0,0))
        pygame.draw.rect(screen,(255,255,255),rectangle)
        screen.blit(text_surface, (60, 470))

        texto_enemigo = team2.get_current_pokemon().name
        texto_amigo = team1.get_current_pokemon().name
        texto_amigo = font.render(texto_amigo, True, (0,0,0))
        texto_enemigo = font.render(texto_enemigo, True, (0,0,0))
        Pokemon_Enemigo(screen, texto_enemigo)
        Pokemon_Amigo(screen, texto_amigo)
        pygame.display.flip()

        wait_next_action()
        turn = 0
        while any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):     
            
            hp_bar(screen, team1.get_current_pokemon(), team2.get_current_pokemon(),background)
            imprimir_pokemons(screen, team1.get_current_pokemon().name, team2.get_current_pokemon().name,team1,team2)
            texto_amigo = team1.get_current_pokemon().name
            Pokemon_Amigo(screen, font.render(team1.get_current_pokemon().name, True, (0,0,0)))
            texto_enemigo = team2.get_current_pokemon().name
            Pokemon_Enemigo(screen, font.render(team2.get_current_pokemon().name, True, (0,0,0)))

            pygame.display.flip()

            action_1, target_1 = team1.get_next_action(team2, effectiveness)
            action_2, target_2 = team2.get_next_action(team1, effectiveness)
            pokemon1 = team1.get_current_pokemon()
            pokemon2= team2.get_current_pokemon()

            # Switching always happens first
            if action_1 == 'switch':
                first = team1
                second = team2
            elif action_2 == 'switch':
                first = team2
                second = team1
                action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
            # If nobody is switching, the fastest pokemon goes firsts

            elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
                first = team1
                second = team2
            else:
                first = team2
                second = team1
                action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1

        
            action_1 = first.return_action(action_1, target_1, second, effectiveness)
            if first == team1:
                pokemon1 = first.get_current_pokemon()
                pokemon2 = second.get_current_pokemon()
            else:
                pokemon1 = second.get_current_pokemon()
                pokemon2 = first.get_current_pokemon()

            hp_bar(screen, pokemon1, pokemon2,background)
            imprimir_accion(screen,action_1,font, pokemon1.name, pokemon2.name,background,team1,team2) 
            wait_next_action() 
            pygame.display.flip()
            # If any of the pokemons fainted, the turn ends, and both have the chance to switch
            if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                if first == team1:
                    pokemon1= first.get_current_pokemon()
                    pokemon2 = second.get_current_pokemon()
                else:
                    pokemon2 = first.get_current_pokemon()
                    pokemon1 = second.get_current_pokemon()

                hp_bar(screen, pokemon1, pokemon2,background)
                faint = team1 if team1.get_current_pokemon().current_hp == 0 else team2
                text = f"{faint.get_current_pokemon().name} fainted!!"
                text_surface = font.render(text, True, (0,0,0))
             
                imprimir_accion(screen,text,font, pokemon1.name, pokemon2.name,background,team1,team2)
                pygame.display.flip()  
                wait_next_action()
                __faint_change__(team1, team2, effectiveness,font,pokemon1,pokemon2,screen,background,pokemon_dict, moves_dict)

            else:
                if action_2 == 'attack' and target_2 is None:
                    action_2, target_2 = second.get_next_action(first, effectiveness)
                action_2 =second.return_action(action_2, target_2, first, effectiveness)

                if first == team1:
                    pokemon1= first.get_current_pokemon()
                    pokemon2 = second.get_current_pokemon()
                else:
                    pokemon2 = first.get_current_pokemon()
                    pokemon1= second.get_current_pokemon()
                hp_bar(screen, pokemon1, pokemon2,background)
                imprimir_accion(screen,action_2,font, pokemon1.name, pokemon2.name,background,team1,team2)
                pygame.display.flip()   
                wait_next_action()
                

                if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                    faint = team1 if team1.get_current_pokemon().current_hp == 0 else team2
                    hp_bar(screen, pokemon1, pokemon2,background)
                    text = f"{faint.get_current_pokemon().name} fainted!!"
                    text_surface = font.render(text, True, (0,0,0))
                    imprimir_accion(screen,text,font, pokemon1.name, pokemon2.name,background,team1,team2)
                
                    pygame.display.flip()  
                    wait_next_action()
                    __faint_change__(team1, team2, effectiveness,font,pokemon1.name,pokemon2.name,screen,background,pokemon_dict, moves_dict)
    
            turn += 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sonidos/Victoria.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2) 
        imprimir_accion(screen,"The battle has ended",font, pokemon1.name, pokemon2.name,background,team1,team2)
        wait_next_action()
        if any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
            imprimir_accion(screen,"You won the battle",font, pokemon1.name, pokemon2.name,background,team1,team2)
        else: 
            imprimir_accion(screen,"You lost the battle",font, pokemon1.name, pokemon2.name,background,team1,team2)
        wait_next_action()
        pygame.quit()

def imprimir_accion(screen: pygame.Surface, accion: str, font: pygame.font.Font, pokemon1, pokemon2,background,team1,team2) -> None:
    screen.blit(background, (0, 0))
    imprimir_pokemons(screen, pokemon1, pokemon2,team1,team2)
    Pokemon_Amigo(screen, font.render(pokemon1, True, (0,0,0)))
    Pokemon_Enemigo(screen, font.render(pokemon2, True, (0,0,0)))
    texto_de_accion(screen, accion, pygame.Rect(30, 450, 680, 65), font)

def __faint_change__(team1, team2, effectiveness,font,pokemon1,pokemon2,screen,background,pokemon_dict, moves_dict, ):
    if team1.get_current_pokemon().current_hp == 0:
        fainted_team = team1
        other_team = team2
    else:
        fainted_team = team2
        other_team = team1
    action_1, target_1 = fainted_team.get_next_action(other_team, effectiveness)
    action_1 =fainted_team.return_action(action_1, target_1, other_team, effectiveness)
    action_2, target_2 = other_team.get_next_action(fainted_team, effectiveness)
    if fainted_team == team1:
        pokemon1 = fainted_team.get_current_pokemon()
        pokemon2 = other_team.get_current_pokemon()
    else:
        pokemon1 = other_team.get_current_pokemon()
        pokemon2 = fainted_team.get_current_pokemon()
     
    hp_bar(screen, pokemon1, pokemon2,background)
    imprimir_accion(screen,action_1,font, pokemon1.name, pokemon2.name,background,team1,team2)
    wait_next_action()
    if action_2 == 'switch':
        action_2 =other_team.return_action(action_2, target_2, fainted_team, effectiveness)
        hp_bar(screen, pokemon1, pokemon2,background)
        imprimir_accion(screen,action_2,font, pokemon1.name, pokemon2.name,background,team1,team2)
        wait_next_action()
      
def wait_next_action():
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
 
def pokemon_to_object(name, poke_list, starter, pokemon_dict, moves_dict): 
    dic = pokedex_number_dict()
    team_temp = []
    for pokemon in poke_list: 
        num_pokedex = int(dic[pokemon])
        team_temp.append(Pokemon.from_dict(num_pokedex,pokemon_dict[num_pokedex],moves_dict))
    best_team = Team(name, team_temp, starter)
    return best_team

def hp_bar(screen: pygame.Surface, pokemon1: Pokemon, pokemon2: Pokemon,background) -> None: #151 es el 100% despues el porcentaje de vida_restante/vida_total va a ser lo que imprimamos en la vida
    largo_total = 151

    vida_total_1, vida_total_2 =  pokemon1.max_hp, pokemon2.max_hp

    vida_restante_1, vida_restante_2 = pokemon1.current_hp, pokemon2.current_hp
    # print (f" {pokemon1.name} vida restante 1: {vida_restante_1}, vida total 1: {vida_total_1}")
    # print (f"{pokemon2.name} vida restante 2: {vida_restante_2}, vida total 2: {vida_total_2}")

    porcentaje1, porcentaje2 = (vida_restante_1/vida_total_1), (vida_restante_2/vida_total_2)

    largo1, largo2 = int(porcentaje1 * largo_total), int(porcentaje2 * largo_total)
    
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
    text2 = "Select best  team"
    button = pygame.transform.scale(pygame.image.load("Interfaz/button.jpg"),(212,98))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 125 <= x <= 125+ 212 and 425<= y <= 425 + 98:
                    return False
                elif 476 <= x <= 476 + 212 and 425 <= y <= 425 + 98:
                    return True
                
        text1_surface = font.render(text1, True, (0,0,0))
        text2_surface = font.render(text2, True, (0,0,0))
        screen.blit(button, (125,400))
        screen.blit(button, (475,400))
        screen.blit(text1_surface, (126, 425))
        screen.blit(text2_surface, (476, 425))  

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
   
def imprimir_pokemons(screen: pygame.Surface, pokemon1: Pokemon, pokemon2: Pokemon,team1:Team,team2:Team,pokedex_dict=pokedex_number_dict(),   ) -> None: 
    pokemon1_number = pokedex_dict[pokemon1].zfill(3)
    pokemon2_number = pokedex_dict[pokemon2].zfill(3)
    x_amigo, x_enemigo = 450, 10
    equipo1_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon1_number}.png'),(200,200))
    equipo2_pokemon_image = pygame.transform.scale(pygame.image.load(f'data/imgs/{pokemon2_number}.png'),(200,200))
    screen.blit(equipo1_pokemon_image, (100, 225))
    screen.blit(equipo2_pokemon_image, (500, 105))

    life_pokeball = pygame.transform.scale(pygame.image.load("Interfaz/pokemon_logo.ico"),(20,20))
    death_pokeball = pygame.transform.scale(pygame.image.load("Interfaz/pokemon_logo2.ico"),(20,20))
    for pokemon in team1.pokemons:
        if pokemon.current_hp > 0:
            screen.blit(life_pokeball, (x_amigo, 270))
        else:
            screen.blit(death_pokeball, (x_amigo, 270))
        x_amigo += 20
    for pokemon in team2.pokemons:
        if pokemon.current_hp > 0:
            screen.blit(life_pokeball, (x_enemigo, 40))
        else:
            screen.blit(death_pokeball, (x_enemigo, 40))
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
    user_team = []
    # user_team = []
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
    if select_best_team_button(screen, font, background_inicio) == True:
        user_team = team[4:]
    else:
        user_team = ingresar_equipo(screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)
       
    user_team = ingresar_equipo(screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)
    user_team = pokemon_to_obj(user_team, moves_dict, pokemon_dict, "user_team")

    opponent_team = menu(elite_1, elite_2, elite_3, elite_4, champion, agus_team, screen,title_font,team_font,font,background_inicio,pokedex_dict,screen_size,user_team)
    
    simulate_battle(user_team, opponent_team, effectiveness_dict, pokemon_dict, moves_dict)
    
    # Update the display

if __name__ == "__main__": 
    main()