from flask import Flask, render_template, request, redirect, url_for
import requests, time, random, base64

app = Flask(__name__)

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

# ---------------------------
# Jinja filter for Base64 encoding
# ---------------------------
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.urlsafe_b64encode(str(s).encode()).decode()

# ---------------------------
# Utility Functions
# ---------------------------
def get_pokemon_data(name_or_id):
    """Fetch Pokémon data from PokeAPI using name or ID."""
    try:
        name_or_id = str(name_or_id).lower()
        r = requests.get(f"{POKEAPI_URL}{name_or_id}")
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "name": d["name"].capitalize(),
            "id": d["id"],
            "icon": d["sprites"]["front_default"],
            "types": [t["type"]["name"].capitalize() for t in d["types"]],
            "abilities": [a["ability"]["name"].capitalize() for a in d["abilities"]],
            "stats": {s["stat"]["name"].capitalize(): s["base_stat"] for s in d["stats"]},
            "weight": d["weight"],
            "height": d["height"]
        }
    except Exception:
        return None

def find_related_pokemon(main_pokemon):
    """Find related Pokémon by type."""
    related = []
    attempts = 0
    while len(related) < 6 and attempts < 50:
        attempts += 1
        rand_id = random.randint(1, 898)
        data = get_pokemon_data(rand_id)
        if not data or data["name"] == main_pokemon["name"]:
            continue
        if any(t in data["types"] for t in main_pokemon["types"]):
            related.append(data)
    return related

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/random")
def random_pokemon():
    random_id = random.randint(1, 898)
    encoded = base64.urlsafe_b64encode(str(random_id).encode()).decode()
    return redirect(url_for("search", q=encoded))

@app.route("/search")
def search():
    q = request.args.get("q", "")
    if not q:
        return redirect(url_for("index"))

    try:
        decoded_q = base64.urlsafe_b64decode(q.encode()).decode()
    except:
        decoded_q = q

    start = time.time()
    pokemon = get_pokemon_data(decoded_q)
    elapsed = round((time.time() - start) * 1000, 2)  # measure only the main fetch

    if not pokemon:
        return render_template("notfound.html")

    # Fetch related after timing
    related = find_related_pokemon(pokemon)
    result_count = len(related) + random.randint(100, 500)


    reencoded = base64.urlsafe_b64encode(decoded_q.encode()).decode()

    return render_template(
        "results.html",
        correct=pokemon,
        related=related,
        elapsed=elapsed,
        count=result_count,
        q_encoded=reencoded
    )

# ---------------------------
# Run the App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
