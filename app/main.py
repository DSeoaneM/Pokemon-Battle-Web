from datetime import datetime
from flask import Flask
from flask_session import Session

from app.routes.trainer_routes import trainer_bp
from app.routes.pokemon_routes import pokemons_bp
from app.routes.battle_routes import battle_bp

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.secret_key = "there are 1025 Pokémon but this site only uses 8"

Session(app)

PROJECT = "POKÉMON Battle Web"
AUTHOR = "David Seoane Miraz"
YEAR = datetime.now().year

app.register_blueprint(trainer_bp)
app.register_blueprint(pokemons_bp, url_prefix="/pokemons")
app.register_blueprint(battle_bp, url_prefix="/battle")

if __name__ == "__main__":
    app.run(port="8080", debug=True)
