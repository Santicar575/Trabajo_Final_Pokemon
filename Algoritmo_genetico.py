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