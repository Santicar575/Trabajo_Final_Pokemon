import pandas as pd
from multiprocessing import Pool
from utils.pokemon import *
from utils.team import *
from utils.combat import *
import random

def random_adn(size_equipo,cant_pokemons):
    adn = []
    for i in range(size_equipo):
        while True:
            pokemon = random.randint(1,cant_pokemons)
            if pokemon not in adn:
                adn.append(pokemon)
                break
    adn.append(random.randint(0,5)) #Se elige que pokemon sale primero de forma aleatoria
    return adn

def iniciar_poblacion(size_equipos,cant_pokemons,population_size):
    return [random_adn(size_equipos,cant_pokemons) for _ in range(population_size)]

def leer_datos():
    moves_dict = {}
    pokemon_dict = {}
    effectiveness_dict = {}
    with open("Trabajo_Final_Pokemon/data/moves.csv") as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line.split(",")
            moves_dict[line[0]] = {"type": line[1], "category": line[2], "pp": int(line[3]),"power":int(line[4]), "accuracy": int(line[5])}
    return moves_dict,pokemon_dict,effectiveness_dict

def fitness(adn,name,moves_dict,pokemon_dict,effectiveness_dict,cant_batallas,cant_pokemons)->int:
    pokemons = [Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(len(adn)-2)] #Creo los pokemons a partir del adn (sin tomar el ultimo elemento del adn ya que es el pokemon starter)
    team = Team(name,pokemons,adn[-1])
    batallas_ganadas = 0
    for i in range(cant_batallas):
        adn_aleatorio = random_adn(len(adn),cant_pokemons)
        pokemons_aleatorios = [Pokemon.from_dict(adn[i],pokemon_dict[adn[i]]) for i in range(len(adn)-2)]
        enemy_team = Team("Enemy_team",pokemons_aleatorios,adn_aleatorio[-1])
        batallas_ganadas += 1 if get_winner(team,enemy_team,effectiveness_dict) == team else 0
    
    return batallas_ganadas

def seleccion_por_ruleta(poblacion,fitness_values)->list[list]:
    total_aptitud = sum(fitness_values)
    seleccionados = []
    for _ in range(len(poblacion) // 2):
        pick = random.uniform(0,total_aptitud)
        current = 0
        for adn,fit in zip(poblacion,fitness_values):
            current += fit
            if current > pick:
                seleccionados.append(adn)
                break
    return seleccionados

def crossover(parent1,parent2,crossover_rate)->tuple[list,list]:
    if crossover_rate >= random.random():
        crossover_point = len(parent1) // 2
        child1 = parent1[0:crossover_point] + parent2[crossover_point:]
        child2 = parent2[0:crossover_point] + parent1[crossover_point:]
        return child1,child2
    else:
        return parent1,parent2

def mutate(adn,mutation_rate,cant_pokemons)->list[int]:
    for i in range(len(adn)-2): #Se mutan todos los pokemons excluyendo al indice del pokemon que sale primero a la batalla
        if mutation_rate >= random.random():
            mutacion = random.randint(1,cant_pokemons)
            adn[i] += mutacion
            adn[i] = adn[i] - cant_pokemons if adn[i] > cant_pokemons else adn[i]
    if mutation_rate >= random.random():
        mutacion = random.randint(0,5)
        adn[-1] += mutacion
        adn[-1] = adn[-1] - 5 if adn[-1] > 5 else adn[-1]
    
    return adn

def main():
    population_size = 52
    cant_pokemons = 801
    size_equipos = 6
    generaciones = 100
    crossover_rate = 0.7
    mutation_rate = 0.03
    cant_batallas = 400

    moves_dict,pokemon_dict,effectiveness_dict = leer_datos()
   
    poblacion_inicial = iniciar_poblacion(size_equipos,cant_pokemons,population_size)

    for generacion in range(generaciones):
        fitness_values = [fitness(adn,moves_dict,pokemon_dict,effectiveness_dict,cant_batallas,cant_pokemons) for adn in poblacion_inicial]
        seleccionados = seleccion_por_ruleta(poblacion_inicial,fitness_values)
        nueva_poblacion = []
        for i in range(population_size//2):
            res1,res2 = crossover(seleccionados[i],seleccionados[i+1],crossover_rate)
            nueva_poblacion.extend([mutate(res1,mutation_rate),mutate(res2,mutation_rate)])
        poblacion_inicial = nueva_poblacion
        
def pruebas():
    adn = random_adn(6,801)
    print(adn)
    adn = mutate(adn,0.03,801)
    print(adn)


if __name__ == "__main__":
    pruebas()
    #main()