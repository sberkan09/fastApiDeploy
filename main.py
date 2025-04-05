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
    Recipe(
        ID=6,
        Name="Recipe 6",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup")
        ],
        TotalTime=10,
        Calories=200,
        Fat=5,
        Protein=5,
        Carbohydrate=30,
        Category="Breakfast",
        Label=["vegan"]
    ),
    Recipe(
        ID=7,
        Name="Recipe 7",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces")
        ],
        TotalTime=15,
        Calories=210,
        Fat=6,
        Protein=6,
        Carbohydrate=31,
        Category="Lunch",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=8,
        Name="Recipe 8",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g")
        ],
        TotalTime=20,
        Calories=220,
        Fat=7,
        Protein=7,
        Carbohydrate=32,
        Category="Dinner",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=9,
        Name="Recipe 9",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices")
        ],
        TotalTime=25,
        Calories=230,
        Fat=8,
        Protein=8,
        Carbohydrate=33,
        Category="Snack",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=10,
        Name="Recipe 10",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g")
        ],
        TotalTime=30,
        Calories=240,
        Fat=9,
        Protein=9,
        Carbohydrate=34,
        Category="Dessert",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=11,
        Name="Recipe 11",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup")
        ],
        TotalTime=10,
        Calories=250,
        Fat=10,
        Protein=10,
        Carbohydrate=35,
        Category="Breakfast",
        Label=["vegan"]
    ),
    Recipe(
        ID=12,
        Name="Recipe 12",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces")
        ],
        TotalTime=15,
        Calories=260,
        Fat=11,
        Protein=11,
        Carbohydrate=36,
        Category="Lunch",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=13,
        Name="Recipe 13",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g")
        ],
        TotalTime=20,
        Calories=270,
        Fat=12,
        Protein=12,
        Carbohydrate=37,
        Category="Dinner",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=14,
        Name="Recipe 14",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices")
        ],
        TotalTime=25,
        Calories=280,
        Fat=13,
        Protein=13,
        Carbohydrate=38,
        Category="Snack",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=15,
        Name="Recipe 15",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g")
        ],
        TotalTime=30,
        Calories=290,
        Fat=14,
        Protein=14,
        Carbohydrate=39,
        Category="Dessert",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=16,
        Name="Recipe 16",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup")
        ],
        TotalTime=10,
        Calories=300,
        Fat=5,
        Protein=15,
        Carbohydrate=40,
        Category="Breakfast",
        Label=["vegan"]
    ),
    Recipe(
        ID=17,
        Name="Recipe 17",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces")
        ],
        TotalTime=15,
        Calories=310,
        Fat=6,
        Protein=16,
        Carbohydrate=41,
        Category="Lunch",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=18,
        Name="Recipe 18",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g")
        ],
        TotalTime=20,
        Calories=320,
        Fat=7,
        Protein=17,
        Carbohydrate=42,
        Category="Dinner",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=19,
        Name="Recipe 19",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices")
        ],
        TotalTime=25,
        Calories=330,
        Fat=8,
        Protein=18,
        Carbohydrate=43,
        Category="Snack",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=20,
        Name="Recipe 20",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g")
        ],
        TotalTime=30,
        Calories=340,
        Fat=9,
        Protein=19,
        Carbohydrate=44,
        Category="Dessert",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=21,
        Name="Recipe 21",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup")
        ],
        TotalTime=10,
        Calories=350,
        Fat=10,
        Protein=5,
        Carbohydrate=45,
        Category="Breakfast",
        Label=["vegan"]
    ),
    Recipe(
        ID=22,
        Name="Recipe 22",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces")
        ],
        TotalTime=15,
        Calories=360,
        Fat=11,
        Protein=6,
        Carbohydrate=46,
        Category="Lunch",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=23,
        Name="Recipe 23",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g")
        ],
        TotalTime=20,
        Calories=370,
        Fat=12,
        Protein=7,
        Carbohydrate=47,
        Category="Dinner",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=24,
        Name="Recipe 24",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices")
        ],
        TotalTime=25,
        Calories=380,
        Fat=13,
        Protein=8,
        Carbohydrate=48,
        Category="Snack",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=25,
        Name="Recipe 25",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g")
        ],
        TotalTime=30,
        Calories=390,
        Fat=14,
        Protein=9,
        Carbohydrate=49,
        Category="Dessert",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=26,
        Name="Recipe 26",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup")
        ],
        TotalTime=10,
        Calories=400,
        Fat=5,
        Protein=10,
        Carbohydrate=30,
        Category="Breakfast",
        Label=["vegan"]
    ),
    Recipe(
        ID=27,
        Name="Recipe 27",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces")
        ],
        TotalTime=15,
        Calories=410,
        Fat=6,
        Protein=11,
        Carbohydrate=31,
        Category="Lunch",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=28,
        Name="Recipe 28",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g")
        ],
        TotalTime=20,
        Calories=420,
        Fat=7,
        Protein=12,
        Carbohydrate=32,
        Category="Dinner",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=29,
        Name="Recipe 29",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=150, unit="g"),
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices")
        ],
        TotalTime=25,
        Calories=430,
        Fat=8,
        Protein=13,
        Carbohydrate=33,
        Category="Snack",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=30,
        Name="Recipe 30",
        Instructions="Step 1: Do something. Step 2: Do something else.",
        Ingredients=[
            Ingredient(name="Rice", quantity=1, unit="cup"),
            Ingredient(name="Tomato", quantity=2, unit="pieces"),
            Ingredient(name="Cheese", quantity=100, unit="g"),
            Ingredient(name="Bread", quantity=2, unit="slices"),
            Ingredient(name="Tofu", quantity=150, unit="g")
        ],
        TotalTime=30,
        Calories=440,
        Fat=9,
        Protein=14,
        Carbohydrate=34,
        Category="Dessert",
        Label=["pescetarian"]
    ),
    Recipe(
        ID=6,
        Name="Recipe 6",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Tomato", quantity=1.15, unit="pieces"),
            Ingredient(name="Carrot", quantity=0.76, unit="g"),
            Ingredient(name="Corn", quantity=1.89, unit="g"),
            Ingredient(name="Tomato", quantity=1.28, unit="pieces")
        ],
        TotalTime=40.8,
        Calories=324,
        Fat=25,
        Protein=14,
        Carbohydrate=82,
        Category="Snack",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=7,
        Name="Recipe 7",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=1.33, unit="g"),
            Ingredient(name="Peas", quantity=1.39, unit="g"),
            Ingredient(name="Mushroom", quantity=0.7, unit="g"),
            Ingredient(name="Carrot", quantity=0.52, unit="g")
        ],
        TotalTime=30.7,
        Calories=408,
        Fat=5,
        Protein=25,
        Carbohydrate=77,
        Category="Snack",
        Label=["vegan", "vegetarian", "vegan"]
    ),
    Recipe(
        ID=8,
        Name="Recipe 8",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Zucchini", quantity=1.8, unit="g"),
            Ingredient(name="Tomato", quantity=1.38, unit="pieces")
        ],
        TotalTime=43.2,
        Calories=473,
        Fat=3,
        Protein=6,
        Carbohydrate=53,
        Category="Dinner",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=9,
        Name="Recipe 9",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Peas", quantity=1.8, unit="g"),
            Ingredient(name="Avocado", quantity=0.87, unit="pieces"),
            Ingredient(name="Peas", quantity=0.75, unit="g")
        ],
        TotalTime=18.3,
        Calories=453,
        Fat=1,
        Protein=2,
        Carbohydrate=34,
        Category="Snack",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=10,
        Name="Recipe 10",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Quinoa", quantity=0.75, unit="g"),
            Ingredient(name="Lentils", quantity=1.28, unit="g"),
            Ingredient(name="Tomato", quantity=1.17, unit="pieces"),
            Ingredient(name="Corn", quantity=1.1, unit="g")
        ],
        TotalTime=31.4,
        Calories=364,
        Fat=22,
        Protein=2,
        Carbohydrate=10,
        Category="Dinner",
        Label=["vegetarian", "vegetarian", "dairy_free"]
    ),
    Recipe(
        ID=11,
        Name="Recipe 11",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=1.61, unit="g"),
            Ingredient(name="Egg", quantity=0.57, unit="pieces"),
            Ingredient(name="Cheese", quantity=0.83, unit="g"),
            Ingredient(name="Peas", quantity=0.93, unit="g")
        ],
        TotalTime=34.6,
        Calories=340,
        Fat=17,
        Protein=15,
        Carbohydrate=31,
        Category="Breakfast",
        Label=["dairy_free"]
    ),
    Recipe(
        ID=12,
        Name="Recipe 12",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Egg", quantity=1.0, unit="pieces"),
            Ingredient(name="Peas", quantity=1.74, unit="g")
        ],
        TotalTime=13.4,
        Calories=272,
        Fat=12,
        Protein=15,
        Carbohydrate=13,
        Category="Snack",
        Label=["vegan"]
    ),
    Recipe(
        ID=13,
        Name="Recipe 13",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Mushroom", quantity=0.7, unit="g"),
            Ingredient(name="Quinoa", quantity=1.3, unit="g"),
            Ingredient(name="Peas", quantity=1.03, unit="g")
        ],
        TotalTime=27.1,
        Calories=198,
        Fat=12,
        Protein=22,
        Carbohydrate=83,
        Category="Lunch",
        Label=["gluten_free", "pescetarian", "vegetarian"]
    ),
    Recipe(
        ID=14,
        Name="Recipe 14",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Beef", quantity=1.64, unit="g"),
            Ingredient(name="Peas", quantity=0.84, unit="g"),
            Ingredient(name="Avocado", quantity=0.76, unit="pieces"),
            Ingredient(name="Tofu", quantity=1.69, unit="g")
        ],
        TotalTime=22.9,
        Calories=195,
        Fat=14,
        Protein=30,
        Carbohydrate=22,
        Category="Breakfast",
        Label=["gluten_free", "gluten_free", "vegan"]
    ),
    Recipe(
        ID=15,
        Name="Recipe 15",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Avocado", quantity=0.97, unit="pieces"),
            Ingredient(name="Zucchini", quantity=1.19, unit="g"),
            Ingredient(name="Zucchini", quantity=0.91, unit="g")
        ],
        TotalTime=44.5,
        Calories=255,
        Fat=6,
        Protein=24,
        Carbohydrate=50,
        Category="Breakfast",
        Label=["gluten_free"]
    ),
    Recipe(
        ID=16,
        Name="Recipe 16",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Avocado", quantity=0.65, unit="pieces"),
            Ingredient(name="Milk", quantity=0.73, unit="cups")
        ],
        TotalTime=21.0,
        Calories=173,
        Fat=23,
        Protein=40,
        Carbohydrate=12,
        Category="Snack",
        Label=["gluten_free", "gluten_free", "vegan"]
    ),
    Recipe(
        ID=17,
        Name="Recipe 17",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Mushroom", quantity=1.43, unit="g"),
            Ingredient(name="Tomato", quantity=0.92, unit="pieces"),
            Ingredient(name="Avocado", quantity=1.4, unit="pieces"),
            Ingredient(name="Beef", quantity=0.88, unit="g")
        ],
        TotalTime=27.7,
        Calories=169,
        Fat=17,
        Protein=25,
        Carbohydrate=57,
        Category="Dessert",
        Label=["vegetarian"]
    ),
    Recipe(
        ID=18,
        Name="Recipe 18",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=1.05, unit="g"),
            Ingredient(name="Mushroom", quantity=1.98, unit="g"),
            Ingredient(name="Peas", quantity=1.09, unit="g"),
            Ingredient(name="Corn", quantity=1.74, unit="g")
        ],
        TotalTime=24.7,
        Calories=681,
        Fat=6,
        Protein=23,
        Carbohydrate=89,
        Category="Lunch",
        Label=["vegan"]
    ),
    Recipe(
        ID=19,
        Name="Recipe 19",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Spinach", quantity=1.24, unit="g"),
            Ingredient(name="Tofu", quantity=0.83, unit="g"),
            Ingredient(name="Carrot", quantity=1.52, unit="g")
        ],
        TotalTime=23.6,
        Calories=664,
        Fat=17,
        Protein=29,
        Carbohydrate=28,
        Category="Snack",
        Label=["dairy_free", "vegan", "vegetarian"]
    ),
    Recipe(
        ID=20,
        Name="Recipe 20",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=1.85, unit="g"),
            Ingredient(name="Lentils", quantity=1.17, unit="g"),
            Ingredient(name="Quinoa", quantity=1.0, unit="g")
        ],
        TotalTime=27.0,
        Calories=237,
        Fat=18,
        Protein=28,
        Carbohydrate=13,
        Category="Breakfast",
        Label=["pescetarian", "vegetarian"]
    ),
    Recipe(
        ID=21,
        Name="Recipe 21",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Lentils", quantity=1.32, unit="g"),
            Ingredient(name="Beef", quantity=1.66, unit="g"),
            Ingredient(name="Spinach", quantity=1.39, unit="g")
        ],
        TotalTime=19.2,
        Calories=675,
        Fat=13,
        Protein=2,
        Carbohydrate=27,
        Category="Breakfast",
        Label=["vegetarian", "vegan"]
    ),
    Recipe(
        ID=22,
        Name="Recipe 22",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Tofu", quantity=0.87, unit="g"),
            Ingredient(name="Quinoa", quantity=0.74, unit="g"),
            Ingredient(name="Beef", quantity=1.54, unit="g")
        ],
        TotalTime=36.5,
        Calories=320,
        Fat=21,
        Protein=7,
        Carbohydrate=79,
        Category="Breakfast",
        Label=["vegetarian", "pescetarian", "pescetarian"]
    ),
    Recipe(
        ID=23,
        Name="Recipe 23",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Spinach", quantity=1.96, unit="g"),
            Ingredient(name="Lentils", quantity=0.55, unit="g"),
            Ingredient(name="Tofu", quantity=1.49, unit="g")
        ],
        TotalTime=21.1,
        Calories=313,
        Fat=11,
        Protein=21,
        Carbohydrate=69,
        Category="Snack",
        Label=["gluten_free", "vegetarian"]
    ),
    Recipe(
        ID=24,
        Name="Recipe 24",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Beef", quantity=1.78, unit="g"),
            Ingredient(name="Beef", quantity=1.15, unit="g"),
            Ingredient(name="Beef", quantity=1.79, unit="g"),
            Ingredient(name="Avocado", quantity=1.85, unit="pieces")
        ],
        TotalTime=41.3,
        Calories=175,
        Fat=1,
        Protein=15,
        Carbohydrate=58,
        Category="Lunch",
        Label=["dairy_free", "vegan"]
    ),
    Recipe(
        ID=25,
        Name="Recipe 25",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Quinoa", quantity=0.57, unit="g"),
            Ingredient(name="Zucchini", quantity=1.05, unit="g")
        ],
        TotalTime=21.7,
        Calories=690,
        Fat=21,
        Protein=29,
        Carbohydrate=40,
        Category="Lunch",
        Label=["pescetarian", "vegan", "vegetarian"]
    ),
    Recipe(
        ID=26,
        Name="Recipe 26",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Cheese", quantity=1.82, unit="g"),
            Ingredient(name="Lentils", quantity=0.97, unit="g"),
            Ingredient(name="Cheese", quantity=1.15, unit="g")
        ],
        TotalTime=25.2,
        Calories=570,
        Fat=3,
        Protein=18,
        Carbohydrate=93,
        Category="Dessert",
        Label=["pescetarian", "pescetarian"]
    ),
    Recipe(
        ID=27,
        Name="Recipe 27",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Peas", quantity=1.77, unit="g"),
            Ingredient(name="Avocado", quantity=1.63, unit="pieces")
        ],
        TotalTime=44.5,
        Calories=627,
        Fat=9,
        Protein=3,
        Carbohydrate=72,
        Category="Lunch",
        Label=["vegan", "dairy_free"]
    ),
    Recipe(
        ID=28,
        Name="Recipe 28",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Lentils", quantity=1.88, unit="g"),
            Ingredient(name="Egg", quantity=1.67, unit="pieces")
        ],
        TotalTime=21.4,
        Calories=590,
        Fat=18,
        Protein=25,
        Carbohydrate=86,
        Category="Breakfast",
        Label=["gluten_free", "gluten_free"]
    ),
    Recipe(
        ID=29,
        Name="Recipe 29",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Mushroom", quantity=1.99, unit="g"),
            Ingredient(name="Peas", quantity=1.48, unit="g"),
            Ingredient(name="Carrot", quantity=1.98, unit="g")
        ],
        TotalTime=13.4,
        Calories=523,
        Fat=1,
        Protein=3,
        Carbohydrate=94,
        Category="Breakfast",
        Label=["pescetarian", "vegetarian"]
    ),
    Recipe(
        ID=30,
        Name="Recipe 30",
        Instructions="Mix the ingredients thoroughly and cook to perfection.",
        Ingredients=[
            Ingredient(name="Peas", quantity=1.03, unit="g"),
            Ingredient(name="Tofu", quantity=0.99, unit="g"),
            Ingredient(name="Mushroom", quantity=1.86, unit="g")
        ],
        TotalTime=27.5,
        Calories=388,
        Fat=8,
        Protein=7,
        Carbohydrate=15,
        Category="Dinner",
        Label=["vegan", "vegetarian"]
    ),
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
