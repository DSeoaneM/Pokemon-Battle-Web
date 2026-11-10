from flask import Blueprint, redirect, render_template, request, session, url_for
from app.decorators.decorators import logged_user
from app.services.pokemon_service import get_pokemons_service, get_pokemon_by_id_service, filter_by_name_service, filter_by_types_service, filter_by_stats_service, filter_by_move_type_service, is_valid_starter_service

pokemons_bp = Blueprint("pokemons", __name__)

@pokemons_bp.route("/", methods=["GET", "POST"])
@logged_user
def pokemon_list():

    filtered_pokemon = get_pokemons_service()

    pokemon_name = request.args.get("pokemon_name", "").strip().lower().replace(" ","-")
    if pokemon_name != "":
        filtered_pokemon = filter_by_name_service(filtered_pokemon, pokemon_name)

    pokemon_types = [request.args.get("pokemon_type_1", "").strip().lower(), request.args.get("pokemon_type_2", "").strip().lower()]
    if pokemon_types[0] != "" or pokemon_types[1] != "":
        filtered_pokemon = filter_by_types_service(filtered_pokemon, pokemon_types)

    pokemon_stats = [
        [request.args.get("pokemon_stat_1", ""), request.args.get("pokemon_stat_1_value", "")],
        [request.args.get("pokemon_stat_2", ""), request.args.get("pokemon_stat_2_value", "")],
        [request.args.get("pokemon_stat_3", ""), request.args.get("pokemon_stat_3_value", "")]
        ]
    for stats in pokemon_stats:
        if stats[0] != "" and stats[1] != "":
            filtered_pokemon = filter_by_stats_service(filtered_pokemon, stats)

    move_type = request.args.get("move_type", "").strip().lower()
    if move_type != "":
        filtered_pokemon = filter_by_move_type_service(filtered_pokemon, move_type)

    if request.method == "POST":
        starter_name = request.form.get("starter_pokemon", "").strip().lower().replace(" ", "-")
        error = []
        if starter_name == "":
            error.append("Choose a Pokémon from the list is mandatory")
        elif not is_valid_starter_service(starter_name):
            error.append("Pokémon name invalid. Choose a Pokémon from the list")
        else:
            session["starter_name"] = starter_name
            return redirect(url_for("battle.battle"))

        session["battle_error"] = error
        return redirect(url_for("pokemons.pokemon_list"))
    
    error = session.pop("battle_error", None)
    return render_template("list.html", error=error, POKEMON_DATA=filtered_pokemon)


@pokemons_bp.route("/<int:id>/")
@logged_user
def pokemon_details(id):
    pokemon_selected = get_pokemon_by_id_service(id)
         
    return render_template("details.html", pokemon=pokemon_selected)
