import json
import random
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from functools import wraps

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

def logged_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer_name" not in session:
            session["login_error"] = ["Introduce your trainer's name to access Pokémon Battle Web"]
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


# ----------
# ROUTES
# ----------
@app.route("/")
def home():
    return render_template("welcome.html", project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = session.pop("login_error", None)
        return render_template("login.html", error=error, project=PROJECT, author=AUTHOR, year=YEAR)

    trainer_name = request.form.get("trainer_name", "").strip()

    error = []
    if not trainer_name:
        error.append("Trainer's name is mandatory")
    elif len(trainer_name) < 3 or len(trainer_name) > 15:
        error.append("Trainer's name length is invalid. It should be between 3 and 15 characters")

    if error:
        session["login_error"] = error
        return redirect(url_for("login"))
    else:
        session["trainer_name"] = trainer_name
        return redirect(url_for("pokemon_list"))

@app.route("/pokemons/", methods=["GET", "POST"])
@logged_user
def pokemon_list():
    filtered_pokemon = POKEMON_DATA

    pokemon_name = request.args.get("pokemon_name", "").strip().lower().replace(" ","-")
    if pokemon_name != "":
        filtered_pokemon = filter_by_name(filtered_pokemon, pokemon_name)

    pokemon_types = [request.args.get("pokemon_type_1", "").strip().lower(), request.args.get("pokemon_type_2", "").strip().lower()]
    if pokemon_types[0] != "" or pokemon_types[1] != "":
        filtered_pokemon = filter_by_types(filtered_pokemon, pokemon_types)

    pokemon_stats = [
        [request.args.get("pokemon_stat_1", ""), request.args.get("pokemon_stat_1_value", "")],
        [request.args.get("pokemon_stat_2", ""), request.args.get("pokemon_stat_2_value", "")],
        [request.args.get("pokemon_stat_3", ""), request.args.get("pokemon_stat_3_value", "")]
        ]
    for stats in pokemon_stats:
        if stats[0] != "" and stats[1] != "":
            filtered_pokemon = filter_by_stats(filtered_pokemon, stats)

    move_type = request.args.get("move_type", "").strip().lower()
    if move_type != "":
        filtered_pokemon = filter_by_move_type(filtered_pokemon, move_type)

    if request.method == "POST":
        starter_name = request.form.get("starter_pokemon", "").strip().lower().replace(" ", "-")
        error = []
        if starter_name != "":
            pokemon_names = []
            for pokemon in POKEMON_DATA:
                pokemon_names.append(pokemon["name"])
            if starter_name in pokemon_names:
                session["starter_name"] = starter_name
                return redirect(url_for("battle"))
            else:
                error.append("Pokémon name invalid. Choose a Pokémon from the list")
        else:
            error.append("Choose a Pokémon from the list is mandatory")

        if error:
            session["battle_error"] = error
            return redirect(url_for("pokemon_list"))
    
    error = session.pop("battle_error", None)
    return render_template("list.html", error=error, POKEMON_DATA=filtered_pokemon, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/pokemons/<int:id>/")
@logged_user
def pokemon_details(id):
    pokemon_selected = None
    for pokemon in POKEMON_DATA:
        if pokemon["id"] == id:
            pokemon_selected = pokemon
         
    return render_template("details.html", pokemon=pokemon_selected, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/battle", methods=["GET"])
@logged_user
def battle():
    if not session.get("starter_name"):
        session["battle_error"] = ["Introduce your starter Pokémon name to access Pokémon Battle Web"]
        return redirect(url_for("pokemon_list"))

    if session.get("starter_pokemon") is None or session["starter_pokemon"]["name"] != session["starter_name"]:
        starter_pokemon = None
        putative_rivals = []
        for pokemon in POKEMON_DATA:
            if pokemon["name"] == session["starter_name"]:
                starter_pokemon = pokemon
            else:
                putative_rivals.append(pokemon)
                    
        rival_pokemon = random.choice(putative_rivals)
        starter_pokemon_moves = random.sample(starter_pokemon["moves"], 4)

        session["starter_pokemon"] = starter_pokemon
        session["starter_pokemon_moves"] = starter_pokemon_moves
        session["rival_pokemon"] = rival_pokemon
    
    return render_template("battle.html")

@app.route("/logout")
@logged_user
def logout():
    session.pop("trainer_name", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(port="8080", debug=True)
