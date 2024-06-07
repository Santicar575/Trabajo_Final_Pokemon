import matplotlib.pyplot as plt
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
    fitness =  []
    with open("best_teams.csv") as csv:
        lines = csv.readlines()
        for line in lines[1:]:
            line = line.strip().split(",")
            equipo = line[4:]
            fitness.append(line[2])
            if line[0] in equipos.keys(): 
                equipos[line[0]] += [equipo]
            else:
                equipos[line[0]] = [equipo]
    return equipos,fitness 

def dic_Pokemons():
    pokemon_dict = {}
    with open("data/pokemons.csv") as file: 
        lines = file.readlines()
        for line in lines[1:]: 
            line = line.strip().split(',')
            pokemon_dict[line[1]] = (line[2],line[3])
    return pokemon_dict



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
    _,fitness = leer_datos_equipos()
    aptitud = []

    for i  in range(len(fitness),50):
        interval = fitness[i:i+50]
        if interval: 
            average = sum(interval)//2 
            aptitud.append(average)  
    x= []
    y = []
    for epoca,ap in enumerate(aptitud):
        x.append(epoca)
        y.append(ap)
    plt.plot(x,y)
    plt.xlabel("Epoch")    
    plt.ylabel("Diversidad")
    plt.title("Fitness evolution through time")
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


def Cant_Pokemons_Epoca_Por_Tipo():
    dic_pokemon = dic_Pokemons()
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    types_colors = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']
<<<<<<< HEAD
    equipos = leer_datos_equipos()
    x, y = types, []
    llaves = equipos.keys()
    cant_tipos = {int(llave): {tipo: 0 for tipo in types} for llave in llaves}
    with open("data/pokemons.csv") as file:
        for equipo in equipos["0"]:
            for pokemon in equipo:
                for tipo in dic_pokemons[pokemon][0]:
                    cant_tipos[0][tipo] += 1
                print(dic_pokemons[pokemon][0])
            
=======
    equipos,_ = leer_datos_equipos()
    cant_tipos = {llave: {tipo: 0 for tipo in types} for llave in equipos.keys()}
    x, y = [int(epoca) for epoca in equipos.keys()], {}
    for epoca in x: #Para cada epoca (50 veces)
        for equipo in equipos[str(epoca)]: #Para cada equipo en cada epoca (50 veces)
            for pokemon in equipo: #Para cada pokemon en cada equipo (6 veces)
                for tipo in dic_pokemon[pokemon]: #Para cada tipo en cada pokemon (1/2 veces)
                    if tipo != '': cant_tipos[str(epoca)][tipo] += 1 #Si tiene tipo, lo cuenta
>>>>>>> 51c90d8c8fa7e1a5b8690c21ff783395c3fefec8

    # Calculate the cumulative sum of pokemon counts for each type
    y = {tipo: [cant_tipos[str(epoca)][tipo] for epoca in x] for tipo in types}
    print(y)
    # Plot the stacked area plot
    plt.stackplot(x, y.values(), labels=y.keys(), colors=types_colors)
    plt.xlabel("Epoch")
    plt.ylabel("Count")
    plt.title("Pokemon Count by Type over Time")
    plt.legend(loc="upper right")
    plt.show()

fitness_evolution()
Cant_Pokemons_Epoca_Por_Tipo()