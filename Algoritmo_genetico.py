from multiprocessing import Pool
from utils.pokemon import *
from utils.team import *
from utils.combat import *
import os
import random
from functools import partial
import numpy as np
import time

def random_adn(size_equipo,cant_pokemons,legendary,pokemon_dict):
    adn = []
    for i in range(size_equipo):
        while True:
            pokemon = random.randint(1,cant_pokemons)
            if pokemon not in adn:
                #Si el pokemon es legendario y no quiero que hayan legendarios (legandary = False) se vuelve a mutar hasta que no sea legendario
                if not legendary and pokemon_dict[pokemon]["is_legendary"]:
                    continue
                else:
                    adn.append(pokemon)
                    break
    adn.append(random.randint(0,5)) #Se elige que pokemon sale primero de forma aleatoria
    return adn

def iniciar_poblacion(size_equipos,cant_pokemons,population_size,legendary,pokemon_dict):
    return [random_adn(size_equipos,cant_pokemons,legendary,pokemon_dict) for _ in range(population_size)]

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


def fitness(adn,moves_dict,pokemon_dict,effectiveness_dict,equipos_aleatorios,adns_aleatorios)->int:
    batallas_ganadas = 0

    #Transforma el adn en objetos de tipo pokemon y luego crea el equipo
    pokemons = [Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(len(adn)-1)] #Crea los pokemons a partir del adn (sin tomar el ultimo elemento del adn ya que es el pokemon starter)
    team = Team("Team",pokemons,adn[-1])
    
    # Realiza las batallas y cuenta las victorias
    resultados = [get_winner(team, Team("Enemy_team", equipo_aleatorio, adn_aleatorio[-1]), effectiveness_dict) == team for equipo_aleatorio, adn_aleatorio in zip(equipos_aleatorios, adns_aleatorios)]
    batallas_ganadas = np.sum(resultados)
    return batallas_ganadas

def parallel_fitness_helper(adn, moves_dict, pokemon_dict, effectiveness_dict,equipos_aleatorios,adns_aleatorios):
    return fitness(adn, moves_dict, pokemon_dict, effectiveness_dict,equipos_aleatorios,adns_aleatorios)

def seleccion(poblacion,fitness_values)->list[list]:
    seleccionados = random.choices(poblacion, fitness_values, k = len(poblacion)//2 + 1)
    # total_aptitud = sum(fitness_values)
    # seleccionados = []
    # for _ in range((len(poblacion) // 2) + 1):
    #     pick = random.uniform(0,total_aptitud)
    #     current = 0
    #     for adn,fit in zip(poblacion,fitness_values):
    #         current += fit
    #         if current > pick:
    #             seleccionados.append(adn)
    #             break
    return seleccionados

def crossover(parent1,parent2,crossover_rate)->tuple[list,list]:
    if crossover_rate >= random.random():
        while True:
            parent1_chance = 0.5
            child1 = [parent1[i] if parent1_chance >= random.random() else parent2[i] for i in range(len(parent1))]
            child2 = [parent1[i] if parent1_chance >= random.random() else parent2[i] for i in range(len(parent1))]
            if len(child1[:6]) == len(set(child1[:6])) and len(child2[:6]) == len(set(child2[:6])):
                break #Si los hijos tienen un pokemon repetido no sale del bucle y se vuelven a generar hasta que tengan todos pokemons ditintos
        return child1,child2
    else:
        return parent1,parent2

def mutate(adn,mutation_rate,cant_pokemons,legendary,pokemon_dict)->list[int]:
    for i in range(len(adn)-2): #Se mutan todos los pokemons excluyendo al indice del pokemon que sale primero a la batalla
        if mutation_rate >= random.random():
            while True: #Sale del bucle si el pokemon a mutar no se encuentra en el equipo, de lo contrario se repite.
                mutacion = random.randint(1,cant_pokemons)
                new_pokemon = adn[i] + mutacion if adn[i] + mutacion <= cant_pokemons else adn[i] + mutacion - cant_pokemons
                if new_pokemon not in adn[:6]:
                    if not legendary and pokemon_dict[new_pokemon]["is_legendary"]: #Si el pokemon es legendario y no quiero que hayan legendarios (legandary = False) se vuelve a mutar hasta que no sea legendario
                        continue
                    else:
                        adn[i] = new_pokemon
                        break

    if mutation_rate >= random.random(): #Hay una probabilidad de mutar el pokemon que sale primero en la batalla
        mutacion = random.randint(0,5)
        adn[-1] += mutacion
        adn[-1] = adn[-1] - 5 if adn[-1] > 5 else adn[-1]
    
    return adn
def quicksort(arr,parametro):
    
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][parametro]
    left = []
    middle = []
    right = []
    for x in arr:
        if x[parametro] > pivot:
            left.append(x)
        elif x[parametro] == pivot:
            middle.append(x)
        else:
            right.append(x)
    return quicksort(left,parametro) + middle + quicksort(right,parametro)


def main():
    population_size = 50
    size_equipos = 6 
    generaciones = 50
    crossover_rate = 0.9
    mutation_rate = 0.03
    cant_batallas = 100
    chunksize = population_size // os.cpu_count() #Se divide la cantidad de tareas que va a realizar cada nucleo dependiendo de la cantidad de nucleos que tenga la pc
    chunksize = chunksize if chunksize > 0 else 1
    legendary = False

    #Se leen los datos de los archivos csv y se guardan en tres diccionarios
    moves_dict,pokemon_dict,effectiveness_dict = leer_datos()
    cant_pokemons = len(pokemon_dict)
   
    #Se inicia la poblacion inicial con equipos aleatorios
    poblacion_inicial = iniciar_poblacion(size_equipos,cant_pokemons,population_size,legendary,pokemon_dict)
    datos = []
    with Pool(os.cpu_count()) as pool: #Se crea un pool con la cantidad de nucleos que tenga la pc del usuario
        #Se itera segun la cantidad de generaciones a realizar
        for generacion in range(generaciones):
            print(f"Generacion {generacion}:")
            ini = time.time()

            # Pre-genera los equipos aleatorios
            adns_aleatorios = [random_adn(size_equipos,cant_pokemons,legendary,pokemon_dict) for _ in range(cant_batallas)]
            equipos_aleatorios = [[Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(size_equipos)] for adn in adns_aleatorios]

            #Se crea una funcion parcial con los argumentos necesarios para luego usar el multiprocesamiento
            partial_fitness = partial(parallel_fitness_helper, moves_dict=moves_dict, 
                                    pokemon_dict=pokemon_dict, effectiveness_dict=effectiveness_dict,
                                    equipos_aleatorios = equipos_aleatorios,adns_aleatorios = adns_aleatorios)
            
            #Se usa la pool para aplicar la funcion parcial a cada adn de la poblacion
            fitness_values = list(pool.imap(partial_fitness, poblacion_inicial,chunksize=chunksize)) #La variable "chunksize" especifica la cantidad de tareas que va a realizar cada nucleo a la vez
            
            datos.append(zip(fitness_values,poblacion_inicial))
            #Se seleccionan los individuos de forma aleatoria (aquellos con mas aptitud tienen mas chances de ser elegidos).
            seleccionados = seleccion(poblacion_inicial,fitness_values)
            nueva_poblacion = []

            for _ in range(population_size//2):
                #se toman dos padres de forma aleatoria de la lista de seleccionados
                parent1 = seleccionados.pop(random.randint(0,len(seleccionados)-1))
                parent2 = seleccionados[random.randint(0,len(seleccionados)-1)]

                #Se cruzan los dos padres 
                res1,res2 = crossover(parent1,parent2,crossover_rate)

                #Se agrega a la nueva poblacion los dos resultados del cruze despues de haber pasado por la funcion de mutacion
                nueva_poblacion.extend([mutate(res1,mutation_rate,cant_pokemons,legendary,pokemon_dict),mutate(res2,mutation_rate,cant_pokemons,legendary,pokemon_dict)])
            
            #La poblacion inicial pasa a ser la nueva poblacion
            poblacion_inicial = nueva_poblacion
            fin=time.time()
            print(fin-ini)

        adns_aleatorios = [random_adn(size_equipos,cant_pokemons,legendary,pokemon_dict) for _ in range(cant_batallas)]
        equipos_aleatorios = [[Pokemon.from_dict(adn[i],pokemon_dict[adn[i]],moves_dict) for i in range(size_equipos)] for adn in adns_aleatorios]
        fitness_values = list(pool.imap(partial_fitness, poblacion_inicial,chunksize=chunksize))
        datos.append(zip(fitness_values,poblacion_inicial))
    
    with open("epochs.csv","w") as epochs:
        with open("best_teams.csv","w") as best_teams:
            best_teams.writelines("epoch,aptitude,team_name,starter,pokemon_1,pokemon_2,pokemon_3,pokemon_4,pokemon_5,pokemon_6\n")
            cant_equipos = [i for i in range(population_size*(generaciones+1))]
            for num_generacion,generacion in enumerate(datos):
                generacion = list(generacion)
                temp_dict = {}
                generacion = quicksort(generacion,0)#el cero representa la posicion por se ordena
                for fit,adn in generacion:
                    for pokemon in adn[:size_equipos]:
                        if pokemon not in temp_dict.keys():
                            temp_dict[pokemon] = 1
                        else:
                            temp_dict[pokemon] += 1
                    pokemons = [pokemon_dict[pokemon]["name"] for pokemon in adn[:size_equipos]]
                    best_teams.writelines(f"{num_generacion},{fit},Team {cant_equipos.pop(0)},{adn[-1]},{','.join(pokemons)}\n")

                cant_pokemons = [",".join([pokemon_dict[pokemon]["name"],str(cant)]) for pokemon,cant in temp_dict.items()]
                cant_pokemons= [elem.split(',') for elem in cant_pokemons]
                cant_pokemons = [[elem[0],int(elem[1])]for elem in cant_pokemons]
                cant_pokemons = quicksort(cant_pokemons,1)
                cant_pokemons = [f'{pokemon[0]},{pokemon[1]}' for pokemon in cant_pokemons]
                epochs.writelines(f"{num_generacion},{len(temp_dict.keys())},{','.join(cant_pokemons)}\n")

if __name__ == "__main__":
    main()