from flask import Blueprint, redirect, render_template, request, session, url_for
from app.decorators.decorators import logged_user
from app.forms.login_form import TrainerLoginForm
from app.main import AUTHOR, PROJECT, YEAR

trainer_bp = Blueprint("trainer", __name__)

@trainer_bp.route("/")
def home():
    return render_template("welcome.html", project=PROJECT, author=AUTHOR, year=YEAR)

@trainer_bp.route("/login", methods=["GET", "POST"])
def login():
    form = TrainerLoginForm()

    if not form.validate_on_submit():
        return redirect(url_for("trainer.login", form=form))
    else:
        return redirect(url_for("pokemons.pokemon_list"))



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
        return redirect(url_for("trainer.login"))
    else:
        session["trainer_name"] = trainer_name
        return redirect(url_for("pokemons.pokemon_list"))

@trainer_bp.route("/logout")
@logged_user
def logout():
    session.pop("trainer_name", None)
    return redirect(url_for("trainer.home"))