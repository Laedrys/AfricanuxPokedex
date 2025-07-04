from flask import Flask, render_template, request
from parser import read_pokemon_entries, get_pokemon_by_name

app = Flask(__name__)
pokemon_data = read_pokemon_entries("pokemon.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    pokemon = get_pokemon_by_name(pokemon_data, query) if query else None
    return render_template("index.html", query=query, pokemon=pokemon)

if __name__ == "__main__":
    app.run(debug=True)
