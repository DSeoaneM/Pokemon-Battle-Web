from app.repositories.pokemon_repository import get_pokemons, get_pokemon_by_id, filter_by_name, filter_by_types, filter_by_stats, filter_by_move_type

def get_pokemons_service():
    return get_pokemons()

def get_pokemon_by_id_service():
    return get_pokemon_by_id()

def filter_by_name_service():
    return filter_by_name()

def filter_by_types_service():
    return filter_by_types()

def filter_by_stats_service():
    return filter_by_stats()

def filter_by_move_type_service():
    return filter_by_move_type()