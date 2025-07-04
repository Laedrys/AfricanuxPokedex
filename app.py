from flask import Flask, render_template, request, jsonify
from parser import read_pokemon_entries, get_pokemon_by_name

app = Flask(__name__)
pokemon_data = read_pokemon_entries("pokemon.txt")

def get_all_types(data):
    types = set()
    for p in data:
        if p.get("Type1"): types.add(p["Type1"])
        if p.get("Type2"): types.add(p["Type2"])
    return sorted(types)

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    sort_by = request.form.get("sort", "number")
    type_filter = request.form.get("type_filter", "").strip()

    filtered_data = pokemon_data
    if type_filter:
        filtered_data = [p for p in filtered_data if p.get("Type1") == type_filter or p.get("Type2") == type_filter]

    if sort_by == "name":
        filtered_data.sort(key=lambda p: p.get("Name", ""))
    else:
        filtered_data.sort(key=lambda p: int(p.get("Number", 0)))

    pokemon = get_pokemon_by_name(filtered_data, query) if query else None
    return render_template("index.html", query=query, pokemon=pokemon, sort_by=sort_by, type_filter=type_filter, types=get_all_types(pokemon_data))

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("query", "").lower()
    matches = [p['Name'] for p in pokemon_data if p['Name'].lower().startswith(query)]
    return jsonify(matches[:10])

if __name__ == "__main__":
    app.run(debug=True)
