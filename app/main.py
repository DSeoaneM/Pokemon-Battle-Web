import json
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

URL_POKEMON_DATA = Path(__file__).resolve().parent.parent / "data" / "pokemons-spooky.json"

with URL_POKEMON_DATA.open(encoding="utf-8") as pokemon_file:
    POKEMON_DATA = json.load(pokemon_file)

@app.route("/")
def home():
    return render_template("welcome.html", project="POKÉMON Battle Web", author="David Seoane Miraz", year=2026)

@app.route("/pokemons/")
def pokemons():
    return render_template("list.html", POKEMON_DATA=POKEMON_DATA, project="POKÉMON Battle Web", author="David Seoane Miraz", year=2026)

@app.route("/pokemons/ID/")
def pokemon_stats(id):
    return render_template("stats.html", id=id, POKEMON_DATA=POKEMON_DATA, project="POKÉMON Battle Web", author="David Seoane Miraz", year=2026)

if __name__ == "__main__":
    app.run(port="8080", debug=True)