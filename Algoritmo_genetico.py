import pandas as pd
from multiprocessing import Pool
from utils.pokemon import *
from utils.team import *
from utils.combat import *
import os
import random
from functools import partial
import numpy as np
import time

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
    """ 
    Crea tres diccionarios con los datos de los movimientos, pokemons y la tabla de efectividad

    Returns:
    moves_dict: Diccionario con los movimientos
    pokemon_dict: Diccionario con los pokemons
    dic_effectiveness_chart: key: tipo1, value: diccionario con la efectividad de cada tipo, donde el diccionario tiene como key el tipo2 y como value la efectividad en float
    """ 
    moves_dict = {}
    pokemon_dict = {}
    dic_effectiveness_chart = {}
    with open ("data/moves.csv")as file: 
        indexs = ((file.readline()).strip()).split(',')
        lines = file.readlines()
        for line in lines: 
            line = line.strip().split(',')
            dic_temp = {}    
            for n_index,index in enumerate(indexs): 
                if n_index !=0: 
                    try : 
                       dic_temp[index]= float(line[n_index])
                    except: 
                        dic_temp[index]= line[n_index]     
              
            moves_dict[line[0]] = dic_temp

    with open("data/effectiveness_chart.csv") as file: 
        indexs = ((file.readline()).strip()).split(',')
        lines = file.readlines()
        for line in lines: 
            line = line.strip().split(',')
            dic_temp = {}    
            for n_index,index in enumerate(indexs): 
                if n_index !=0: 
                    dic_temp[index]= float(line[n_index])
            dic_effectiveness_chart[line[0]]= dic_temp
        
    with open("data/pokemons.csv") as file: 
        indexs= (file.readline().strip()).split(",")
        lines = file.readlines()
        for line in lines: 
            line = line.strip().split(',')
            dic_temp = {}    
            for n_index,index in enumerate(indexs): 
                if n_index !=0: 
                    if index == "moves": 
                        var_temp = line[n_index].split(";")
                        dic_temp[index] = var_temp
                    else: 
                        try : 
                            dic_temp[index]= float(line[n_index])
                        except:
                            dic_temp[index]= line[n_index]
            pokemon_dict[int(line[0])] = dic_temp
    return moves_dict,pokemon_dict,dic_effectiveness_chart


def fitness(adn,moves_dict,pokemon_dict,effectiveness_dict,cant_batallas,cant_pokemons)->int:
    pokemons = [Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(len(adn)-1)] #Creo los pokemons a partir del adn (sin tomar el ultimo elemento del adn ya que es el pokemon starter)
    team = Team("Team",pokemons,adn[-1])
    batallas_ganadas = 0

    # Pre-genera los equipos aleatorios
    adns_aleatorios = [random_adn(len(adn)-1, cant_pokemons) for _ in range(cant_batallas)]
    equipos_aleatorios = [[Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(len(adn)-1)] for adn in adns_aleatorios]

    # Realiza las batallas y cuenta las victorias
    resultados = [get_winner(team, Team("Enemy_team", equipo_aleatorio, adn_aleatorio[-1]), effectiveness_dict) == team for equipo_aleatorio, adn_aleatorio in zip(equipos_aleatorios, adns_aleatorios)]
    batallas_ganadas = np.sum(resultados)
    return batallas_ganadas

def parallel_fitness_helper(adn, moves_dict, pokemon_dict, effectiveness_dict, cant_batallas, cant_pokemons):
    return fitness(adn, moves_dict, pokemon_dict, effectiveness_dict, cant_batallas, cant_pokemons)

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
        while True:
            parent1_chance = 0.5
            child1 = [parent1[i] if parent1_chance >= random.random() else parent2[i] for i in range(len(parent1))]
            child2 = [parent1[i] if parent1_chance >= random.random() else parent2[i] for i in range(len(parent1))]
            if len(child1[:6]) == len(set(child1[:6])) and len(child2[:6]) == len(set(child2[:6])):
                break #Si los hijos tienen un pokemon resultado no sale del bucle y se vuelven a generar hasta que tengan todos pokemons ditintos
        return child1,child2
    else:
        return parent1,parent2

def mutate(adn,mutation_rate,cant_pokemons)->list[int]:
    for i in range(len(adn)-2): #Se mutan todos los pokemons excluyendo al indice del pokemon que sale primero a la batalla
        if mutation_rate >= random.random():
            while True: #Sale del bucle si el pokemon a mutar no se encuentra en el equipo, de lo contrario se repite.
                mutacion = random.randint(1,cant_pokemons)
                new_pokemon = adn[i] + mutacion if adn[i] + mutacion <= cant_pokemons else adn[i] + mutacion - cant_pokemons
                if new_pokemon not in adn:
                    adn[i] = new_pokemon
                    break

    if mutation_rate >= random.random():
        mutacion = random.randint(0,5)
        adn[-1] += mutacion
        adn[-1] = adn[-1] - 5 if adn[-1] > 5 else adn[-1]
    
    return adn

def main():
    population_size = 50
    cant_pokemons = 801
    size_equipos = 6
    generaciones = 10
    crossover_rate = 0.9
    mutation_rate = 0.03
    cant_batallas = 5

    moves_dict,pokemon_dict,effectiveness_dict = leer_datos()
   
    poblacion_inicial = iniciar_poblacion(size_equipos,cant_pokemons,population_size)
    with Pool(os.cpu_count()) as pool:
        for generacion in range(generaciones):
            print(f"Generacion {generacion}:")
            ini = time.time()
            partial_fitness = partial(parallel_fitness_helper, moves_dict=moves_dict, 
                                  pokemon_dict=pokemon_dict, effectiveness_dict=effectiveness_dict, 
                                  cant_batallas=cant_batallas, cant_pokemons=cant_pokemons)
            fitness_values = list(pool.imap(partial_fitness, poblacion_inicial,chunksize=10))
            
            #fitness_values = pool.map( lambda adn: fitness(adn,moves_dict,pokemon_dict,effectiveness_dict,cant_batallas,cant_pokemons),poblacion_inicial)
            seleccionados = seleccion_por_ruleta(poblacion_inicial,fitness_values)
            nueva_poblacion = []
            for i in range(population_size//2):
                res1,res2 = crossover(seleccionados[i-1],seleccionados[i],crossover_rate)
                nueva_poblacion.extend([mutate(res1,mutation_rate,cant_pokemons),mutate(res2,mutation_rate,cant_pokemons)])
            poblacion_inicial = nueva_poblacion
            fin=time.time()
            print(fin-ini)
    
    fitness_values = [fitness(adn,moves_dict,pokemon_dict,effectiveness_dict,cant_batallas,cant_pokemons) for adn in poblacion_inicial]
    with open("Prueva.csv","w") as f:
        f.writelines("Aptitud,Equipo\n")
        for fit,adn in zip(fitness_values,poblacion_inicial):
            team = []
            for i in range(len(adn)-1):
                team.append(pokemon_dict[adn[i]]["name"])
            f.writelines(f"{fit},{team}\n")

if __name__ == "__main__":
    main()