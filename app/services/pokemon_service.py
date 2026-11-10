import random

from app.repositories.pokemon_repository import get_pokemons, get_pokemon_by_id, get_pokemon_by_name, filter_by_name, filter_by_types, filter_by_stats, filter_by_move_type

def get_pokemons_service():
    return get_pokemons()

def get_pokemon_by_id_service(id):
    return get_pokemon_by_id(id)

def get_pokemon_by_name_service(name):
    return get_pokemon_by_name(name)

def filter_by_name_service(pokemon_list, pokemon_name):
    return filter_by_name(pokemon_list, pokemon_name)

def filter_by_types_service(pokemon_list, pokemon_type):
    return filter_by_types(pokemon_list, pokemon_type)

def filter_by_stats_service(pokemon_list, pokemon_stat):
    return filter_by_stats(pokemon_list, pokemon_stat)

def filter_by_move_type_service(pokemon_list, move_type):
    return filter_by_move_type(pokemon_list, move_type)

def is_valid_starter_service(starter_name):
    return get_pokemon_by_name(starter_name) is not None

def prepare_battle_service(starter_name):
    starter_pokemon = get_pokemon_by_name(starter_name)

    putative_rivals = []
    for pokemon in get_pokemons():
        if pokemon.name != starter_name:
            putative_rivals.append(pokemon)

    rival_pokemon = random.choice(putative_rivals)
    starter_pokemon_moves = random.sample(starter_pokemon.moves, 4)

    return starter_pokemon, starter_pokemon_moves, rival_pokemon