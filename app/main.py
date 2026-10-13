import json
import random
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
            if (stat["name"] == pokemon_stat and stat["value"] >= int(pokemon_stat_value)):
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
@app.route("/")
def home():
    return render_template("welcome.html", project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", project=PROJECT, author=AUTHOR, year=YEAR)

    trainer_name = request.form.get("trainer_name", "").strip()
    error = None
    if not trainer_name:
        error = "Trainer's name is mandatory"
    elif len(trainer_name) < 3 or len(trainer_name) > 15:
        error = "Trainer's name length is invalid. It should be between 3 and 15 characters"

    if error:
        return render_template("login.html", error=error, trainer_name=trainer_name, project=PROJECT, author=AUTHOR, year=YEAR)

    return redirect(url_for("pokemon_list", trainer_name=trainer_name))

@app.route("/pokemons", methods=["GET", "POST"])
def pokemon_list():
    trainer_name = request.args.get("trainer_name")

    if request.method == "GET":
        return render_template("list.html", trainer_name=trainer_name, POKEMON_DATA=POKEMON_DATA, project=PROJECT, author=AUTHOR, year=YEAR)

    if request.method == "POST":
        trainer_name = request.form.get("trainer_name") or trainer_name

    filtered_pokemon = POKEMON_DATA

    pokemon_name = request.form.get("pokemon_name", "").strip().lower()
    # if pokemon_name != "":
    #     for pokemon in POKEMON_DATA:
    #         if pokemon_name in pokemon["name"] and pokemon not in filtered_pokemon:
    #             filtered_pokemon.append(pokemon)
    if pokemon_name != "":
        filtered_pokemon = filter_by_name(filtered_pokemon, pokemon_name)


    # pokemon_type_1 = request.form.get("pokemon_type_1", "").strip().lower()
    # pokemon_type_2 = request.form.get("pokemon_type_2", "").strip().lower()
    pokemon_types = [request.form.get("pokemon_type_1", "").strip().lower(), request.form.get("pokemon_type_2", "").strip().lower()]
    # for pokemon in POKEMON_DATA:
    #     if pokemon_type_1 == pokemon_type_2 and [pokemon_type_1] == pokemon["types"] and pokemon not in filtered_pokemon:
    #         filtered_pokemon.append(pokemon)
    #     elif pokemon_type_1 in pokemon["types"] and pokemon_type_2 == "" and pokemon not in filtered_pokemon:
    #         filtered_pokemon.append(pokemon)
    #     elif pokemon_type_1 != pokemon_type_2 and pokemon_type_1 in pokemon["types"] and pokemon_type_2 in pokemon["types"] and pokemon not in filtered_pokemon:
    #         filtered_pokemon.append(pokemon)
    if pokemon_types[0] != "" or pokemon_types[1] != "":
        filtered_pokemon = filter_by_types(filtered_pokemon, pokemon_types)


    # pokemon_stat_1 = request.form.get("pokemon_stat_1", "")
    # pokemon_stat_1_value = request.form.get("pokemon_stat_1_value", "")
    # pokemon_stat_2 = request.form.get("pokemon_stat_2", "")
    # pokemon_stat_2_value = request.form.get("pokemon_stat_2_value", "")
    # pokemon_stat_3 = request.form.get("pokemon_stat_3", "")
    # pokemon_stat_3_value = request.form.get("pokemon_stat_3_value", "")
    pokemon_stats = [
        [request.form.get("pokemon_stat_1", ""), request.form.get("pokemon_stat_1_value", "")],
        [request.form.get("pokemon_stat_2", ""), request.form.get("pokemon_stat_2_value", "")],
        [request.form.get("pokemon_stat_3", ""), request.form.get("pokemon_stat_3_value", "")]
        ]
    
    for stats in pokemon_stats:
        if stats[0] != "" and stats[1] != "":
            filtered_pokemon = filter_by_stats(filtered_pokemon, stats)

    # pokemon_con_stat_1 = []
    # pokemon_con_stat_2 = []
    # pokemon_con_stat_3 = []
    # for pokemon in POKEMON_DATA:
    #     for stat in pokemon["stats"]:
    #         if (stat["name"] == pokemon_stat_1 and stat["value"] >= int(pokemon_stat_1_value)):
    #             pokemon_con_stat_1.append(pokemon)   

    # if pokemon_stat_2 != "":
    #     for pokemon in pokemon_con_stat_1:
    #         for stat in pokemon["stats"]:
    #             if (stat["name"] == pokemon_stat_2 and stat["value"] >= int(pokemon_stat_2_value)):
    #                 pokemon_con_stat_2.append(pokemon)
    
    # if pokemon_stat_3 != "":    
    #     for pokemon in pokemon_con_stat_2:
    #         for stat in pokemon["stats"]:
    #             if (stat["name"] == pokemon_stat_3 and stat["value"] >= int(pokemon_stat_3_value)):
    #                 pokemon_con_stat_3.append(pokemon)

    # if pokemon_stat_3 != "":
    #     for pokemon in pokemon_con_stat_3:
    #         if pokemon not in filtered_pokemon:
    #             filtered_pokemon.append(pokemon)
    # elif pokemon_stat_2 != "":
    #     for pokemon in pokemon_con_stat_2:
    #         if pokemon not in filtered_pokemon:
    #             filtered_pokemon.append(pokemon)
    # else:
    #         for pokemon in pokemon_con_stat_1:
    #             if pokemon not in filtered_pokemon:
    #                 filtered_pokemon.append(pokemon)


    move_type = request.form.get("move_type", "").strip().lower()
    # if move_type != "":
    #     for pokemon in POKEMON_DATA:
    #         for move in pokemon["moves"]:
    #             if move_type == move["type"] and pokemon not in filtered_pokemon:
    #                 filtered_pokemon.append(pokemon)
    if move_type != "":
        filtered_pokemon = filter_by_move_type(filtered_pokemon, move_type)


    starter_name = request.form.get("starter_pokemon", "").strip().lower().replace(" ", "-")
    if starter_name != "":
        pokemon_names = []
        error = []
        for pokemon in POKEMON_DATA:
            pokemon_names.append(pokemon["name"])
        if starter_name in pokemon_names:
            return redirect(url_for("battle", trainer_name=trainer_name, starter_name=starter_name))
        else:
            error.append("Pokémon name invalid. Choose a Pokémon from the list")

        if error:
            return render_template("list.html", error=error, trainer_name=trainer_name, POKEMON_DATA=filtered_pokemon, project=PROJECT, author=AUTHOR, year=YEAR)

    return render_template("list.html", trainer_name=trainer_name, POKEMON_DATA=filtered_pokemon, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/pokemons/<int:id>/")
def pokemon_details(id):
    trainer_name = request.args.get("trainer_name")
    pokemon_selected = None
    for pokemon in POKEMON_DATA:
        if pokemon["id"] == id:
            pokemon_selected = pokemon

    if pokemon_selected == None:
        return render_template("details.html", trainer_name=trainer_name, pokemon=pokemon_selected, project=PROJECT, author=AUTHOR, year=YEAR)
            
    return render_template("details.html", trainer_name=trainer_name, pokemon=pokemon_selected, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/battle", methods=["GET"])
def battle():
    trainer_name = request.args.get("trainer_name")
    starter_name = request.args.get("starter_name")
    starter_pokemon = None
    putative_rivals = []

    for pokemon in POKEMON_DATA:
        if pokemon["name"] == starter_name:
            starter_pokemon = pokemon
        else:
            putative_rivals.append(pokemon)

    rival_pokemon = random.choice(putative_rivals)

    starter_pokemon_moves = random.sample(starter_pokemon["moves"], 4)
    rival_pokemon_moves = random.sample(rival_pokemon["moves"], 4)

    return render_template("battle.html", 
                           trainer_name=trainer_name, 
                           starter_pokemon=starter_pokemon, 
                           starter_pokemon_moves=starter_pokemon_moves, 
                           rival_pokemon=rival_pokemon, 
                           rival_pokemon_moves=rival_pokemon_moves)

if __name__ == "__main__":
    app.run(port="8080", debug=True)
