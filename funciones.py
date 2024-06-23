from utils.team import * 
from utils.pokemon import *
from utils.combat import *

#//////////////////////////////////////////////
#PARA EL ALGORITMO GENETICO

def leer_datos() -> tuple:
    """ 
    Crea tres diccionarios con los datos de los movimientos, pokemons y la tabla de efectividad

    Returns:
    - moves_dict: Diccionario con los movimientos
    - pokemon_dict: Diccionario con los pokemons
    - dic_effectiveness_chart: Diccionario con la efectividad de cada tipo de pokemon
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

def pokedex_number_dict() -> dict:
    """
    Lee el archivo 'pokemons.csv' y crea un diccionario que mapea los nombres de los Pokémon con sus números de la Pokédex.

    Returns:
    - pokedex_number_dict: Diccionario que mapea los nombres de los Pokémon con sus números de la Pokédex.
    """
    pokedex_number_dict = {}
    with open("data/pokemons.csv") as file:
        file.readline()
        for line in file:
            line = line.strip().split(",")
            pokedex_number_dict[line[1]] = line[0]
    return pokedex_number_dict

#//////////////////////////////////////////////
#PARA LOS GRAFICOS

def leer_epochs() -> dict:
    """
    Lee el archivo "epochs.csv" y devuelve un diccionario con la información de los epochs.

    Returns:
    - epochs: Diccionario con la información de los epochs. {num_epoch: (valores).
    """
    epochs = {}
    with open("csv_generados/epochs.csv") as file: 
        lines = file.readlines() 
        for line in lines: 
            line = line.strip().split(",")
            dic= {}
            for i in range(2, len(line),2): 
                dic[line[i]] = int(line[i+1])
            epochs[int(line[0])] = [int(line[1]), dic]
    return epochs

def leer_datos_equipos() -> dict:
    """
    Lee los datos de los equipos desde un archivo CSV y los devuelve en un diccionario.

    Returns:
    - equipos: Un diccionario que contiene los equipos y sus datos.
    """
    equipos = {}
    with open("csv_generados/best_teams.csv") as csv:
        lines = csv.readlines()
        for line in lines[1:]:
            line = line.strip().split(",")
            equipo = line[4:]
            if line[0] in equipos.keys(): 
                equipos[line[0]] += [equipo]
            else:
                equipos[line[0]] = [equipo]
    return equipos

def dic_Pokemons() -> dict:
    """
    Esta función devuelve un diccionario que contiene información sobre los pokémones.
    
    Returns:
    - pokemon_dict: Diccionario con los nombres de los pokémones y la información adicional sobre cada pokémon. {nombre_pokemon: (tipo1, tipo2)}
    """
    pokemon_dict = {}
    with open("data/pokemons.csv") as file: 
        lines = file.readlines()
        for line in lines[1:]: 
            line = line.strip().split(',')
            pokemon_dict[line[1]] = (line[2],line[3])
    return pokemon_dict

def fitness_dic_from_csv() -> dict:
    """
    Lee el archivo CSV llamado 'best_teams.csv' y crea un diccionario de fitness.

    Returns:
    - fitnes_dic: Diccionario que contiene los valores de fitness de los equipos. {nombre_equipo: [fitness]}
    """
    fitnes_dic =  {}
    with open("csv_generados/best_teams.csv") as csv:
        lines = csv.readlines()
        for line in lines[1:len(lines)]: 
            line = line.strip().split(",")
            if line[0] in fitnes_dic:  
                fitnes_dic[line[0]].append(int(line[1]))
            else:
                fitnes_dic[line[0]]= [int(line[1])]
    return fitnes_dic

def get_best_team(population_size: int) -> list:
    """
    Obtiene el mejor equipo de Pokémon de acuerdo al tamaño de la población.

    Parámetros:
    - population_size: Tamaño de la población.

    Retorna:
    - best_team: Lista con los nombres de los Pokémon del mejor equipo.
    """
    with open("csv_generados/best_teams.csv") as f:
        lines = f.readlines()
        best_team = lines[:-1*(population_size+1):-1][-1].strip().split(",")
    return best_team
