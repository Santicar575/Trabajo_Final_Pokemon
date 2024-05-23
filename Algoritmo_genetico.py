import pandas as pd
from multiprocessing import Pool
from utils.pokemon import *
import random

def random_adn(size_equipo,cant_pokemons):
    adn = []
    for i in range(size_equipo):
        while True:
            pokemon = random.randint(1,cant_pokemons)
            if pokemon not in adn:
                adn.append(pokemon)
                break
    return adn

def iniciar_poblacion(size_equipos,cant_pokemons,population_size):
    return [random_adn(size_equipos,cant_pokemons) for _ in range(population_size)]

def leer_datos():
    moves_dict = {}
    with open("Trabajo_Final_Pokemon/data/moves.csv") as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line.split(",")
            moves_dict[line[0]] = {"type": line[1], "category": line[2], "pp": int(line[3]),"power":int(line[4]), "accuracy": int(line[5])}
    return moves_dict

def fitness()->int:
    pass

def seleccion_por_ruleta(poblacion,fitness_values)->list[list]:
    pass

def crossover(parent1,parent2,crossover_rate)->tuple[list,list]:
    pass

def mutate(adn,mutation_rate)->list[list]:
    pass

def main():
    population_size = 52
    cant_pokemons = 811
    size_equipos = 6
    generaciones = 100
    crossover_rate = 0.7
    mutation_rate = 0.03

    pokemon_df = pd.read_csv("Trabajo_Final_Pokemon/data/pokemons.csv")
    pokemon_df["moves"] = pokemon_df["moves"].apply(lambda x: str(x).split(";"))
    pokemon_dict = pokemon_df.to_dict(orient="records")
    moves_dict = leer_datos()
   
    poblacion_inicial = iniciar_poblacion(size_equipos,cant_pokemons,population_size)

    for generacion in range(generaciones):
        fitness_values = [fitness(adn) for adn in poblacion_inicial]
        seleccionados = seleccion_por_ruleta(poblacion_inicial,fitness_values)
        nueva_poblacion = []
        for i in range(population_size//2):
            res1,res2 = crossover(seleccionados[i],seleccionados[i+1],crossover_rate)
            nueva_poblacion.extend([mutate(res1,mutation_rate),mutate(res2,mutation_rate)])
        poblacion_inicial = nueva_poblacion
        

if __name__ == "__main__":
    main()