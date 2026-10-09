import json
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

@app.route("/")
def home():
    return render_template("welcome.html", project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", project=PROJECT, author=AUTHOR, year=YEAR)

    trainer_name = request.form.get("trainer", "").strip()
    error = None
    if not trainer_name:
        error = "Trainer's name is mandatory"
    elif len(trainer_name) < 3 or len(trainer_name) > 15:
        error = "Trainer's name length is invalid. It should be between 3 and 15 characters"

    if error:
        return render_template("login.html", error=error, name=trainer_name, project=PROJECT, author=AUTHOR, year=YEAR)

    return redirect(url_for("pokemon_list", name=trainer_name))

@app.route("/pokemons/")
def pokemon_list():
    trainer_name = request.args["name"]
    return render_template("list.html", name=trainer_name, POKEMON_DATA=POKEMON_DATA, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/pokemons/<int:id>/")
def pokemon_details(id):
    pokemon_selected = None
    for pokemon in POKEMON_DATA:
        if pokemon["id"] == id:
            pokemon_selected = pokemon
    return render_template("details.html", pokemon=pokemon_selected, project=PROJECT, author=AUTHOR, year=YEAR)

if __name__ == "__main__":
    app.run(port="8080", debug=True)