import matplotlib.pyplot as plt
import numpy as np 
from Algoritmo_genetico import leer_datos

def leer_epochs():
    epochs = {}
    with open("epochs.csv") as file: 
        lines = file.readlines() 
        for line in lines: 
            line = line.strip().split(",")
            dic= {}
            for i in range(2, len(line),2): 
                dic[line[i]] = int(line[i+1])
            epochs[int(line[0])] = [int(line[1]), dic]
    return epochs

def leer_datos_equipos():
    equipos: dict = {}
    with open("best_teams.csv") as csv:
        lines = csv.readlines()
        for line in lines[1:]:
            line = line.strip().split(",")
            equipo = line[4:]
            if line[0] in equipos.keys(): 
                equipos[line[0]] += [equipo]
            else:
                equipos[line[0]] = [equipo]
    return equipos 

def dic_Pokemons():
    pokemon_dict = {}
    with open("data/pokemons.csv") as file: 
        lines = file.readlines()
        for line in lines[1:]: 
            line = line.strip().split(',')
            pokemon_dict[line[1]] = (line[2],line[3])
    return pokemon_dict

def pokedex_number_dict():
    pokedex_number_dict = {}
    with open("data/pokemons.csv") as file:
        file.readline()
        for line in file:
            line = line.strip().split(",")
            pokedex_number_dict[line[1]] = line[0]
    return pokedex_number_dict

def fitness_dic_from_csv():
    fitnes_dic =  {}
    with open("best_teams.csv") as csv:
        lines = csv.readlines()
        for line in lines[1:len(lines)]: 
            line = line.strip().split(",")
            if line[0] in fitnes_dic:  
                fitnes_dic[line[0]].append(int(line[1]))
            else:
                fitnes_dic[line[0]]= [int(line[1])]
    return fitnes_dic

def get_best_team(population_size):
    with open("best_teams.csv") as f:
        #f.readline()
        lines = f.readlines()
        best_team = lines[:-1*(population_size+1):-1][-1].strip().split(",")
    return best_team

def dic_id_pokemon(): 
    dic= {}
    with open("data/pokemons.csv") as csv: 
        lines = csv.readlines() 
    for line in lines[1:]: 
        line = line.strip().split(',')
        dic[line[1]] = line[0]
    return dic

def diversity_vs_epoch(): # grafico 1
    epochs = leer_epochs()
    x = []
    y = []
    for epoch in epochs: 
        x.append(epoch)
        y.append(epochs[epoch][0])
    plt.plot(x, y)
    plt.xlabel("Epoch")
    plt.ylabel("Diversidad")
    plt.title("Diversidad vs Epoch")
    plt.show()


def fitness_evolution(): #grafico 2 
    dic_fitness = fitness_dic_from_csv()
    x = []
    y = []
    for epoch in dic_fitness: 
        x.append(epoch)
        y.append(sum(dic_fitness[epoch])//50) 
    plt.plot(x,y)
    plt.xlabel("Epoch")
    plt.ylabel("Fitness")
    plt.title("Fitness Evolution")
    plt.show()
    

def pokemons_in_last_generation(): #grafico 3
    epochs = leer_epochs() 
    x = [] 
    y = [] 
    for pokemons in epochs[50][1]: 
        x.append(pokemons)
        y.append(epochs[50][1][pokemons])
    fig, ax = plt.subplots()
    ax.barh(x, width = y)
    ax.invert_yaxis()
    plt.xlabel("Count")
    plt.ylabel("Pokemons")
    plt.show()


def Cant_Pokemons_Epoca_Por_Tipo(): #Grafico 4 
    dic_pokemon = dic_Pokemons()
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    types_colors = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']
    equipos = leer_datos_equipos()
    cant_tipos = {llave: {tipo: 0 for tipo in types} for llave in equipos.keys()}
    x, y = [int(epoca) for epoca in equipos.keys()], {}
    for epoca in x: #Para cada epoca (50 veces)
        for equipo in equipos[str(epoca)]: #Para cada equipo en cada epoca (50 veces)
            for pokemon in equipo: #Para cada pokemon en cada equipo (6 veces)
                for tipo in dic_pokemon[pokemon]: #Para cada tipo en cada pokemon (1/2 veces)
                    if tipo != '': cant_tipos[str(epoca)][tipo] += 1 #Si tiene tipo, lo cuenta


    # Calculate the cumulative sum of pokemon counts for each type
    y = {tipo: [cant_tipos[str(epoca)][tipo] for epoca in x] for tipo in types}
    #print(y)
    # Plot the stacked area plot
    plt.stackplot(x, y.values(), labels=y.keys(), colors=types_colors)
    plt.xlabel("Epoch")
    plt.ylabel("Count")
    plt.title("Pokemon Count by Type over Time")
    plt.legend(loc="upper right")
    plt.show()

def best_team_stats(): #Grafico 6 
    best_team= get_best_team(50)
    dic_id = dic_id_pokemon()
    _,dic_pokemones,_ = leer_datos()
    subjects = ['hp','attack','defense','sp_attack','sp_defense','speed']
    stats =[]
    for pokemon in best_team[4:]:
        poke_stats = []
        for subject in subjects: 
            poke_stats.append(dic_pokemones[int(dic_id[pokemon])][subject])
        poke_stats = np.concatenate((poke_stats,[poke_stats[0]]))
        stats.append(poke_stats)

    num_vars = len(stats[0]) 
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=True).tolist() #angles in radians
    print(angles)
    plt.figure(figsize=(6,6))
    plt.subplot(polar = True)
    for stat in stats: 
        plt.plot(angles,stat)
    plt.xticks(angles[:-1],subjects)
    plt.legend(best_team[4:],loc ='best')
    plt.show()
        
def show_best_team(best_team:list[str],pokemon_dict):
    dic_pokemon = dic_Pokemons()
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    types_colors = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']
    best_team = best_team[2:]
    team_name = best_team.pop(0)
    starter = int(best_team.pop(0))
    plt.suptitle(f"Best team: {team_name}", fontsize=10)
    for i,pokemon in enumerate(best_team):
        pokedex_number = str(pokemon_dict[pokemon])
        pokedex_number = pokedex_number.zfill(3) 
        img = plt.imread(f"data/imgs/{pokedex_number}.png", format="png")
        #Se crea una grilla de 2x3 subplots con la imagen de cada pokemon
        plt.subplot(2, 3, i+1)
        plt.imshow(img)
        plt.axis("off")
        plt.text(0.5, -0.1, f"{pokemon} {'(starter)'if i == starter else ''}", size=10, ha="center", transform=plt.gca().transAxes)  # Add text below each image
        pokemon_types = [type for type in dic_pokemon[pokemon] if type in types]
        if len(pokemon_types) == 1:
            plt.text(0.5, -0.3, pokemon_types[0], size=8, ha="center",
                transform=plt.gca().transAxes, 
                bbox=dict(facecolor=types_colors[types.index(pokemon_types[0])], alpha=0.5))
        elif len(pokemon_types) == 2:
            plt.text(0.3, -0.3, pokemon_types[0], size=8, ha="center",
                transform=plt.gca().transAxes, 
                bbox=dict(facecolor=types_colors[types.index(pokemon_types[0])], alpha=0.5))
            plt.text(0.7, -0.3, pokemon_types[1], size=8, ha="center",
                transform=plt.gca().transAxes, 
                bbox=dict(facecolor=types_colors[types.index(pokemon_types[1])], alpha=0.5))
    plt.show()

def main():
    population_size = 50
    while True:
        n = int(input("1. Diversidad vs Epoch\n2. Fitness Evolution\n3. Pokemons in last generation\n4. Pokemon count by type over time\n5. \n6. Best team stats\n7. Show best team\n8. Exit\n"))
        match(n):
            case 1:
                diversity_vs_epoch()
            case 2:
                fitness_evolution()
            case 3:
                pokemons_in_last_generation()
            case 4:
                Cant_Pokemons_Epoca_Por_Tipo()
            case 5:
                pass
            case 6:
                best_team_stats()
            case 7:
                show_best_team(get_best_team(population_size),pokedex_number_dict())
            case 8:
                break
            case _:
                print("Opcion invalida")
    
    pass

if __name__ == "__main__":
    main()
