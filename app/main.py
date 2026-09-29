from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"Bienvenido a la Batalla Pokémon entrenador"

if __name__ == "__main__":
    app.run(port="8080", debug=True)