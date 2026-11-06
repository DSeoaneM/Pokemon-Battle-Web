import json
import random
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from functools import wraps

from app.decorators.decorators import logged_user
from app.routes.trainer_routes import trainer_bp
from app.routes.pokemon_routes import pokemons_bp
from app.routes.battle_routes import battle_bp

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.secret_key = "there are 1025 Pokémon but this site only uses 8"

Session(app)

PROJECT = "POKÉMON Battle Web"
AUTHOR = "David Seoane Miraz"
YEAR = datetime.now().year

URL_POKEMON_DATA = Path(__file__).resolve().parent.parent / "data" / "pokemons-spooky.json"

with URL_POKEMON_DATA.open(encoding="utf-8") as pokemon_file:
    POKEMON_DATA = json.load(pokemon_file)

# ----------
# FUNCTIONS
# ----------
def filter_by_name(pokemon_list, pokemon_name):
    filtered_pokemon = []

    for pokemon in pokemon_list:
        if len(pokemon_name) <= 2 and pokemon["name"].startswith(pokemon_name):
            filtered_pokemon.append(pokemon)
        elif len(pokemon_name) > 2 and pokemon_name in pokemon["name"]:
            filtered_pokemon.append(pokemon)

    return filtered_pokemon

def filter_by_types(pokemon_list, pokemon_types):
    pokemon_type_1 = pokemon_types[0]
    pokemon_type_2 = pokemon_types[1]   
    filtered_pokemon = []

    for pokemon in pokemon_list:
        if pokemon_type_1 == pokemon_type_2 and [pokemon_type_1] == pokemon["types"]:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_1 in pokemon["types"] and pokemon_type_2 == "" and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_2 in pokemon["types"] and pokemon_type_1 == "" and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)
        elif pokemon_type_1 != pokemon_type_2 and pokemon_type_1 in pokemon["types"] and pokemon_type_2 in pokemon["types"] and pokemon not in filtered_pokemon:
            filtered_pokemon.append(pokemon)

    return filtered_pokemon

def filter_by_stats(pokemon_list, pokemon_stats):
    pokemon_stat = pokemon_stats[0]
    pokemon_stat_value = pokemon_stats[1]
    
    filtered_pokemon = []  
    
    for pokemon in pokemon_list:
        for stat in pokemon["stats"]:
            if stat["name"] == pokemon_stat and stat["value"] >= int(pokemon_stat_value):
                filtered_pokemon.append(pokemon)   

    return filtered_pokemon

def filter_by_move_type(pokemon_list, move_type):
    filtered_pokemon = []

    for pokemon in pokemon_list:
        for move in pokemon["moves"]:
            if move_type == move["type"] and pokemon not in filtered_pokemon:
                filtered_pokemon.append(pokemon)

    return filtered_pokemon

# ----------
# ROUTES
# ----------

app.register_blueprint(trainer_bp)
app.register_blueprint(pokemons_bp, url_prefix="/pokemons")
app.register_blueprint(battle_bp, url_prefix="/battle")

if __name__ == "__main__":
    app.run(port="8080", debug=True)
