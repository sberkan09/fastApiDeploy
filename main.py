from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

app = FastAPI(title="Dummy Recipe Backend")

# CORS desteği (mobil uygulama testleri için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modeller
class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

class Recipe(BaseModel):
    ID: int
    Name: str
    Instructions: str
    Ingredients: List[Ingredient] = []
    TotalTime: float = 0.0
    Calories: float
    Fat: float
    Protein: float
    Carbohydrate: float
    Category: str
    Label: List[str] = []

class Preferences(BaseModel):
    dairy_free: bool
    gluten_free: bool
    pescetarian: bool
    vegan: bool
    vegetarian: bool

class UserPreferences(BaseModel):
    user_id: str
    preferences: Preferences

class UserAllergies(BaseModel):
    user_id: str
    allergies: List[str]

# Dummy veriler
dummy_categories = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"]

dummy_recipes = [
    Recipe(
        ID=1,
        Name="Vegan Pancakes",
        Instructions="Mix all ingredients and fry on medium heat.",
        Ingredients=[
            Ingredient(name="Flour", quantity=2, unit="cups"),
            Ingredient(name="Almond Milk", quantity=1.5, unit="cups")
        ],
        TotalTime=15.0,
        Calories=350,
        Fat=5,
        Protein=8,
        Carbohydrate=70,
        Category="Breakfast",
        Label=["vegan", "vegetarian", "dairy_free"]
    ),
    Recipe(
        ID=2,
        Name="Chicken Salad",
        Instructions="Mix grilled chicken with fresh vegetables. Mix grilled chicken with fresh vegetables. Mix grilled chicken with fresh vegetables. Mix grilled chicken with fresh vegetables. Mix grilled chicken with fresh vegetables.",
        Ingredients=[
            Ingredient(name="Chicken Breast", quantity=200, unit="g"),
            Ingredient(name="Lettuce", quantity=100, unit="g")
        ],
        TotalTime=20.0,
        Calories=450,
        Fat=10,
        Protein=35,
        Carbohydrate=10,
        Category="Lunch",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=3,
        Name="Gluten-Free Brownies",
        Instructions="Mix ingredients and bake for 25 minutes.",
        Ingredients=[
            Ingredient(name="Gluten-Free Flour", quantity=1, unit="cup"),
            Ingredient(name="Cocoa Powder", quantity=0.5, unit="cup")
        ],
        TotalTime=30.0,
        Calories=500,
        Fat=20,
        Protein=6,
        Carbohydrate=65,
        Category="Dessert",
        Label=["gluten_free", "vegetarian"]
    ),
    Recipe(
        ID=4,
        Name="Seafood Pasta",
        Instructions="Cook pasta and mix with shrimp and scallops.",
        Ingredients=[
            Ingredient(name="Pasta", quantity=200, unit="g"),
            Ingredient(name="Shrimp", quantity=150, unit="g")
        ],
        TotalTime=25.0,
        Calories=600,
        Fat=15,
        Protein=30,
        Carbohydrate=80,
        Category="Dinner",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=5,
        Name="Fruit Salad",
        Instructions="Chop assorted fruits and mix.",
        Ingredients=[
            Ingredient(name="Apple", quantity=1, unit="piece"),
            Ingredient(name="Banana", quantity=1, unit="piece"),
            Ingredient(name="Orange", quantity=1, unit="piece")
        ],
        TotalTime=10.0,
        Calories=200,
        Fat=1,
        Protein=2,
        Carbohydrate=50,
        Category="Snack",
        Label=["vegan", "vegetarian", "gluten_free", "dairy_free"]
    ),
    # İstediğin kadar dummy tarif ekleyebilirsin...
]

# Kullanıcı tercihler ve alerji verilerini saklamak için in-memory veritabanı (sözlük)
user_preferences_db: Dict[str, UserPreferences] = {}
user_allergies_db: Dict[str, UserAllergies] = {}

dummy_preferences = ["dairy_free", "gluten_free", "pescetarian", "vegan", "vegetarian"]
dummy_allergies = ["Peanuts", "Tree Nuts", "Dairy", "Eggs", "Shellfish", "Soy", "Wheat"]

# API Endpoints

@app.get("/getCategories")
def get_categories():
    return dummy_categories

@app.get("/getUserRecommendations")
def get_user_recommendations():
    # Hepsi sana tavsiye: tüm dummy tarifler!
    return dummy_recipes

@app.get("/getRecipeDetails")
def get_recipe_details(recipe_id: int):
    for recipe in dummy_recipes:
        if recipe.ID == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@app.get("/getRecipeCard")
def get_recipe_card(recipe_id: int, fields: List[str] = Query(...)):
    recipe = next((r for r in dummy_recipes if r.ID == recipe_id), None)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe_dict = recipe.dict()
    # Sadece istenen alanları döndür
    filtered_card = {field: recipe_dict.get(field) for field in fields if field in recipe_dict}
    return filtered_card

@app.get("/getPreferences")
def get_preferences():
    return dummy_preferences

@app.get("/getUserPreferences")
def get_user_preferences(user_id: str):
    if user_id in user_preferences_db:
        return user_preferences_db[user_id]
    # Daha önce ayarlanmamışsa default tercihler gönder
    default_prefs = Preferences(
        dairy_free=False,
        gluten_free=False,
        pescetarian=False,
        vegan=False,
        vegetarian=False
    )
    default_user_prefs = UserPreferences(user_id=user_id, preferences=default_prefs)
    user_preferences_db[user_id] = default_user_prefs
    return default_user_prefs

@app.post("/setUserPreferences")
def set_user_preferences(preferences: UserPreferences):
    user_preferences_db[preferences.user_id] = preferences
    return {"message": "User preferences updated", "data": preferences}

@app.get("/query")
def query_recipes(
    query: str,
    sortBy_field: str = Query(..., alias="sortBy.field"),
    sortBy_direction: str = Query(..., alias="sortBy.direction")
):
    try:
        query_dict = json.loads(query)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid query JSON")
    
    filtered = dummy_recipes

    # Arama kelimesine göre filtrele
    search_term = query_dict.get("search", "").lower()
    if search_term:
        filtered = [r for r in filtered if search_term in r.Name.lower()]
    
    # Kategori filtresi
    if "category" in query_dict:
        category = query_dict["category"].lower()
        filtered = [r for r in filtered if r.Category.lower() == category]

    # Diyet filtreleri
    for filt in ["vegan", "vegetarian", "gluten_free", "dairy_free", "pescetarian"]:
        if query_dict.get(filt, False):
            filtered = [r for r in filtered if filt in r.Label]

    # Sıralama
    reverse = sortBy_direction.lower() == "desc"
    try:
        filtered.sort(key=lambda r: getattr(r, sortBy_field), reverse=reverse)
    except Exception:
        pass

    return filtered

@app.get("/getAllergies")
def get_allergies():
    return dummy_allergies

@app.get("/getUserAllergies")
def get_user_allergies(user_id: str):
    if user_id in user_allergies_db:
        return user_allergies_db[user_id]
    default_allergies = UserAllergies(user_id=user_id, allergies=[])
    user_allergies_db[user_id] = default_allergies
    return default_allergies

@app.post("/setUserAllergies")
def set_user_allergies(allergies: UserAllergies):
    user_allergies_db[allergies.user_id] = allergies
    return {"message": "User allergies updated", "data": allergies}

# Uygulamayı çalıştırmak için (terminalden: uvicorn main:app --reload)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
