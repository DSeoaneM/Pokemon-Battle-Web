import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template

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

@app.route("/pokemons/")
def pokemon_list():
    return render_template("list.html", POKEMON_DATA=POKEMON_DATA, project=PROJECT, author=AUTHOR, year=YEAR)

@app.route("/pokemons/<int:id>/")
def pokemon_details(id):
    pokemon_selected = None
    for pokemon in POKEMON_DATA:
        if pokemon["id"] == id:
            pokemon_selected = pokemon
    return render_template("details.html", pokemon=pokemon_selected, project=PROJECT, author=AUTHOR, year=YEAR)

if __name__ == "__main__":
    app.run(port="8080", debug=True)