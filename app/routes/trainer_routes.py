from flask import Blueprint, redirect, render_template, request, session, url_for
from app.decorators.decorators import logged_user
from app.forms.login_form import TrainerLoginForm

trainer_bp = Blueprint("trainer", __name__)

@trainer_bp.route("/")
def home():

    return render_template("welcome.html")

@trainer_bp.route("/login", methods=["GET", "POST"])
def login():

    if "trainer_name" in session:
        return redirect(url_for("pokemons.pokemon_list"))
    
    form = TrainerLoginForm()

    if request.method == "GET":
        error = session.pop("login_error", None)
        return render_template("login.html",form=form, error=error)
    
    if form.validate_on_submit():
        session["trainer_name"] = form.trainer_name.data
        return redirect(url_for("pokemons.pokemon_list"))

    return render_template("login.html", form=form, error=None)
        
@trainer_bp.route("/logout")
@logged_user
def logout():
    session.clear()
    return redirect(url_for("trainer.home"))