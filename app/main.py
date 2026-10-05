import json
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

RUTA_DATOS_POKEMON = Path(__file__).resolve().parent.parent / "data" / "pokemons-spooky.json"

with RUTA_DATOS_POKEMON.open(encoding="utf-8") as fichero_pokemon:
    DATOS_POKEMON = json.load(fichero_pokemon)

@app.route("/")
def home():
    return render_template("welcome.html", project="POKÉMON Battle Web", author="David Seoane Miraz", year=2026)

@app.route("/pokemons/")
def pokemon():
    return render_template("bienvenida.html", DATOS_POKEMON=DATOS_POKEMON, proyecto="POKÉMON Battle Web", autor="David Seoane Miraz", año=2026)

if __name__ == "__main__":
    app.run(port="8080", debug=True)