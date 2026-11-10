from flask import Blueprint, redirect, render_template, session, url_for
from app.decorators.decorators import logged_user
from app.services.pokemon_service import prepare_battle_service

battle_bp = Blueprint("battle", __name__)

@battle_bp.route("", methods=["GET"])
@logged_user
def battle():
    if not session.get("starter_name"):
        session["battle_error"] = ["Introduce your starter Pokémon name to access Pokémon Battle Web"]
        return redirect(url_for("pokemons.pokemon_list"))

    if session.get("starter_pokemon") is None or session["starter_pokemon"].name != session["starter_name"]:
        starter_pokemon, starter_pokemon_moves, rival_pokemon = prepare_battle_service(session["starter_name"])
        session["starter_pokemon"] = starter_pokemon
        session["starter_pokemon_moves"] = starter_pokemon_moves
        session["rival_pokemon"] = rival_pokemon
    
    return render_template("battle.html")
