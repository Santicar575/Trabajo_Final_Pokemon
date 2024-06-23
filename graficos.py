import matplotlib.pyplot as plt
import numpy as np 
from funciones import *

def diversity_vs_epoch() -> None: #Grafico 1
    """
    Genera un gráfico que muestra la diversidad en función de las épocas.
    
    Esta función lee las épocas desde un archivo y utiliza los datos para generar un gráfico de línea.
    El eje x representa las épocas y el eje y representa la diversidad en cada época.
    """
    epochs, x, y  = leer_epochs(), [], []
    for epoch in epochs: 
        x.append(epoch)
        y.append(epochs[epoch][0])
    plt.plot(x, y)
    plt.xlabel("Epoch")
    plt.ylabel("Diversidad")
    plt.title("Diversidad vs Epoch")
    plt.show()

def fitness_evolution() -> None: #Grafico 2
    """
    Genera un gráfico que muestra la evolución del fitness a lo largo de las épocas.

    La función lee un diccionario de fitness desde un archivo CSV y utiliza los datos
    para generar un gráfico de línea que muestra cómo el fitness ha cambiado a lo largo
    del tiempo. El eje x representa las épocas y el eje y representa el fitness promedio
    para cada época.
    """
    dic_fitness, x, y = fitness_dic_from_csv(), [], []
    for epoch in dic_fitness: 
        x.append(epoch)
        y.append(sum(dic_fitness[epoch])//50) 
    plt.plot(x,y)
    plt.xlabel("Epoch")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness")
    plt.show()
    
def pokemons_in_last_generation() -> None: #Grafico 3
    """
    Genera un gráfico de barras horizontales que muestra la cantidad de pokemons de la última generación.
    
    La función lee los datos de las épocas y extrae la información de la última época.
    Luego, crea dos listas, una con los nombres de los pokemons y otra con la cantidad de cada uno.
    """
    epochs, x, y = leer_epochs(), [], [] 
    for pokemons in epochs[50][1]: 
        x.append(pokemons)
        y.append(epochs[50][1][pokemons])
    _, ax = plt.subplots()
    ax.barh(x, width = y)
    ax.invert_yaxis()
    plt.xlabel("Count")
    plt.ylabel("Pokemons")
    plt.show()

def type_in_last_generation() -> None: #Grafico 4
    """
    Genera un gráfico de barras horizontales que muestra la cantidad de Pokémon de cada tipo en la última generación.

    Utiliza datos de epochs y dic_pokemon para obtener la información necesaria.
    Los tipos de Pokémon se representan con colores específicos.
    """
    epochs, dic_pokemon, x, y = leer_epochs(), dic_Pokemons(), [], []
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    types_colors = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']
    dic_colores = {tipo: color for tipo, color in zip(types, types_colors)}
    cant_tipos = {tipo: 0 for tipo in types}
    for pokemon in epochs[50][1]:
        for tipo in dic_pokemon[pokemon]: 
            if tipo != '':
                cant_tipos[tipo] += 1
    cant_tipos_ordenado = dict(sorted(cant_tipos.items(), key=lambda item: item[1], reverse=True))

    for tipo in cant_tipos_ordenado.keys():
        x.append(tipo)
        y.append(cant_tipos[tipo])
    fig, ax = plt.subplots()
    ax.barh(x, width=y)
    ax.invert_yaxis()
    colors = [dic_colores[tipo] for tipo in x]
    ax.barh(x, width=y, color=colors)
    plt.xlabel("Count")
    plt.ylabel("Pokemons")
    plt.show()

def Cant_Pokemons_Epoca_Por_Tipo() -> None: #Grafico 5
    """
    Genera un gráfico de barras apiladas que muestra la cantidad de Pokémon por tipo a lo largo del tiempo.

    Utiliza un diccionario de Pokémon y un diccionario de equipos para obtener la información necesaria.
    Los tipos de Pokémon se definen en una lista llamada 'types' y los colores correspondientes se definen en una lista llamada 'types_colors'.
    """
    dic_pokemon, equipos = dic_Pokemons(), leer_datos_equipos()
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    types_colors = ['#A8A77A', '#EE8130', '#6390F0', '#F7D02C', '#7AC74C', '#96D9D6', '#C22E28', '#A33EA1', '#E2BF65', '#A98FF3', '#F95587', '#A6B91A', '#B6A136', '#735797', '#6F35FC', '#705746', '#B7B7CE', '#D685AD']
    cant_tipos = {llave: {tipo: 0 for tipo in types} for llave in equipos.keys()}
    x, y = [int(epoca) for epoca in equipos.keys()], {}
    for epoca in x:
        for equipo in equipos[str(epoca)]:
            for pokemon in equipo:
                for tipo in dic_pokemon[pokemon]:
                    if tipo != '':
                        cant_tipos[str(epoca)][tipo] += 1
    y = {tipo: [cant_tipos[str(epoca)][tipo] for epoca in x] for tipo in types}
    plt.stackplot(x, y.values(), labels=y.keys(), colors=types_colors)
    plt.xlabel("Epoch")
    plt.ylabel("Count")
    plt.title("Pokemon Count by Type over Time")
    plt.legend(loc="upper right")
    plt.show()

def best_team_stats() -> None: #Grafico 6
    """
    Genera un gráfico polar que muestra las estadísticas de los mejores equipos de Pokémon.

    La función obtiene los mejores equipos y un diccionario de números de Pokédex.
    Luego, lee los datos de los Pokémon y crea una lista de estadísticas para cada Pokémon del equipo.
    """
    best_team, dic_id= get_best_team(50), pokedex_number_dict()
    _, dic_pokemones, _ = leer_datos()
    subjects = ['hp','attack','defense','sp_attack','sp_defense','speed']
    stats = []
    for pokemon in best_team[4:]:
        poke_stats = []
        for subject in subjects: 
            poke_stats.append(dic_pokemones[int(dic_id[pokemon])][subject])
        poke_stats = np.concatenate((poke_stats,[poke_stats[0]]))
        stats.append(poke_stats)

    num_vars = len(stats[0]) 
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=True).tolist() #angles in radians
    plt.figure(figsize=(6,6))
    plt.subplot(polar = True)
    for stat in stats: 
        plt.plot(angles,stat)
    plt.xticks(angles[:-1],subjects)
    plt.legend(best_team[4:],loc ='best')
    plt.show()
        
def show_best_team(best_team: list, pokemon_dict) -> None: #Grafico 7
    """
    Consigue las imágenes de los Pokémon y los tipos de cada uno para mostrarlos en un gráfico. 
    Luego, muestra el mejor equipo de Pokémon en forma de gráfico.

    Parámetros:
    - best_team: Una lista de cadenas que representa el mejor equipo de Pokémon.
    - pokemon_dict: Un diccionario que mapea nombres de Pokémon a números de la Pokédex.
    """
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
    print(get_best_team(50))
    while True:
        n = int(input("1. Diversidad vs Epoch\n2. Fitness Evolution\n3. Pokemons in last generation\n4. Type count in last generation\n5. Pokemon count by type over time\n6. Best team stats\n7. Show best team\n8. Exit\n"))
        match(n):
            case 1:
                diversity_vs_epoch()
            case 2:
                fitness_evolution()
            case 3:
                pokemons_in_last_generation()
            case 4:
                type_in_last_generation()
            case 5:
                Cant_Pokemons_Epoca_Por_Tipo()
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
