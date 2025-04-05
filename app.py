from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy veri modelleri
recipes = {
    1: {
        "id": 1,
        "name": "Spaghetti Bolognese",
        "description": "Lezzetli İtalyan makarnası",
        "ingredients": ["pasta", "domates", "kıyma"]
    },
    2: {
        "id": 2,
        "name": "Chicken Curry",
        "description": "Baharatlı ve aromatik tavuk yemeği",
        "ingredients": ["tavuk", "köri", "pirinç"]
    }
}

user_preferences_db = {}  # Örnek: {"user1": {"user_id": "user1", "preferences": ["Vegan", "Glutensiz"]}}
user_allergies_db = {}    # Örnek: {"user1": {"user_id": "user1", "allergies": ["Yer fıstığı", "Kabuklu deniz ürünleri"]}}

@app.route("/getCategories", methods=["GET"])
def get_categories():
    return jsonify(["İtalyan", "Hint", "Meksika", "Çin"])

@app.route("/getUserRecommendations", methods=["GET"])
def get_user_recommendations():
    return jsonify(list(recipes.values()))

@app.route("/getRecipeDetails", methods=["GET"])
def get_recipe_details():
    recipe_id = request.args.get("recipe_id", type=int)
    recipe = recipes.get(recipe_id)
    if recipe:
        return jsonify(recipe)
    else:
        return jsonify({"error": "Tarif bulunamadı"}), 404

@app.route("/getRecipeCard", methods=["GET"])
def get_recipe_card():
    recipe_id = request.args.get("recipe_id", type=int)
    fields = request.args.getlist("fields")
    recipe = recipes.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Tarif bulunamadı"}), 404
    recipe_card = {field: recipe.get(field) for field in fields if field in recipe}
    return jsonify(recipe_card)

@app.route("/getPreferences", methods=["GET"])
def get_preferences():
    return jsonify(["Vegetaryen", "Vegan", "Glutensiz", "Süt ürünleri içermeyen"])

@app.route("/getUserPreferences", methods=["GET"])
def get_user_preferences():
    user_id = request.args.get("user_id")
    prefs = user_preferences_db.get(user_id)
    if prefs is None:
        prefs = {"user_id": user_id, "preferences": []}
    return jsonify(prefs)

@app.route("/setUserPreferences", methods=["POST"])
def set_user_preferences():
    data = request.get_json()
    if data and "user_id" in data:
        user_preferences_db[data["user_id"]] = data
        return jsonify({"message": "Kullanıcı tercihleri başarıyla güncellendi."})
    else:
        return jsonify({"error": "Geçersiz veri."}), 400

@app.route("/query", methods=["GET"])
def query_recipes():
    query_json = request.args.get("query")  # Dummy örnek, kullanmıyoruz
    sort_field = request.args.get("sortBy.field")
    sort_direction = request.args.get("sortBy.direction", "asc")
    recipe_list = list(recipes.values())
    reverse = sort_direction.lower() == "desc"
    if sort_field:
        try:
            recipe_list.sort(key=lambda x: x.get(sort_field), reverse=reverse)
        except Exception as e:
            pass
    return jsonify(recipe_list)

@app.route("/getAllergies", methods=["GET"])
def get_allergies():
    return jsonify(["Yer fıstığı", "Kabuklu deniz ürünleri", "Gluten", "Soya"])

@app.route("/getUserAllergies", methods=["GET"])
def get_user_allergies():
    user_id = request.args.get("user_id")
    allergies = user_allergies_db.get(user_id)
    if allergies is None:
        allergies = {"user_id": user_id, "allergies": []}
    return jsonify(allergies)

@app.route("/setUserAllergies", methods=["POST"])
def set_user_allergies():
    data = request.get_json()
    if data and "user_id" in data:
        user_allergies_db[data["user_id"]] = data
        return jsonify({"message": "Kullanıcı alerji bilgileri başarıyla güncellendi."})
    else:
        return jsonify({"error": "Geçersiz veri."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
