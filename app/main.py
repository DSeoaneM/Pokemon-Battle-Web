from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("bienvenida.html", proyecto="POKÉMON Battle Web", autor="David Seoane Miraz", año=2026)

if __name__ == "__main__":
    app.run(port="8080", debug=True)