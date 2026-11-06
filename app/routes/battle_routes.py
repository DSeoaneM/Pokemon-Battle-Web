import random
from flask import Blueprint, redirect, render_template, session, url_for
from app.decorators.decorators import logged_user
from app.repositories.pokemon_repository import load_data

battle_bp = Blueprint("battle", __name__)

@battle_bp.route("", methods=["GET"])
@logged_user
def battle():
    if not session.get("starter_name"):
        session["battle_error"] = ["Introduce your starter Pokémon name to access Pokémon Battle Web"]
        return redirect(url_for("pokemons.pokemon_list"))

    if session.get("starter_pokemon") is None or session["starter_pokemon"]["name"] != session["starter_name"]:
        starter_pokemon = None
        putative_rivals = []
        for pokemon in load_data():
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
