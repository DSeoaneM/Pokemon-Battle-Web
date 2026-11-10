import json
from pathlib import Path
from app.models.pokemon import Pokemon

URL_POKEMON_DATA = Path(__file__).resolve().parent.parent.parent / "data" / "pokemons-spooky.json"

def load_data():
    with URL_POKEMON_DATA.open(encoding="utf-8") as pokemon_file:
        return json.load(pokemon_file)  

def get_pokemons():
    pokemons = []
    for pokemon in load_data():
        pokemons.append(Pokemon(pokemon["id"], pokemon["name"], pokemon["types"], pokemon["weight"], pokemon["height"], pokemon["sprites"], pokemon["stats"], pokemon["moves"]))
    return pokemons  

def get_pokemon_by_id(id):
    for pokemon in get_pokemons():
        if pokemon.id == id:
            return pokemon
    return None

def get_pokemon_by_name(name):
    for pokemon in get_pokemons():
        if pokemon.name == name:
            return pokemon
    return None

def filter_by_name(pokemon_list, pokemon_name):
    filtered_pokemon = []

    for pokemon in pokemon_list:
        if len(pokemon_name) <= 2 and pokemon.name.startswith(pokemon_name):
            filtered_pokemon.append(pokemon)
        elif len(pokemon_name) > 2 and pokemon_name in pokemon.name:
            filtered_pokemon.append(pokemon)

    return filtered_pokemon


def filter_by_types(pokemon_list, pokemon_types):
    pokemon_type_1 = pokemon_types[0]
    pokemon_type_2 = pokemon_types[1]   
    filtered_pokemon = []

    for pokemon in pokemon_list:
        if pokemon_type_1 == pokemon_type_2 and [pokemon_type_1] == pokemon.types:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_1 in pokemon.types and pokemon_type_2 == "" and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_2 in pokemon.types and pokemon_type_1 == "" and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_1 != pokemon_type_2 and pokemon_type_1 in pokemon.types and pokemon_type_2 in pokemon.types and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)

    return filtered_pokemon


def filter_by_stats(pokemon_list, pokemon_stats):
    pokemon_stat = pokemon_stats[0]
    pokemon_stat_value = pokemon_stats[1]
    
    filtered_pokemon = []  
    
    for pokemon in pokemon_list:
        for stat in pokemon.stats:
            if stat["name"] == pokemon_stat and stat["value"] >= int(pokemon_stat_value):
                filtered_pokemon.append(pokemon)   

    return filtered_pokemon


def filter_by_move_type(pokemon_list, move_type):
    filtered_pokemon = []

    for pokemon in pokemon_list:
        for move in pokemon.moves:
            if move_type == move["type"] and pokemon not in filtered_pokemon:
                filtered_pokemon.append(pokemon)

    return filtered_pokemon