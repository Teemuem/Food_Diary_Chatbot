from spellchecker import SpellChecker
from api_utils import fetch_nutrient_data
import numpy as np 

def clean_ai_output(food_items):
    spell = SpellChecker()  # Initialize the spell checker

    for item in food_items:
        # Correct typos in the food name
        food_name = item.get("food_name", "")
        corrected_food_name = " ".join([spell.correction(word) for word in food_name.split()])
        item["food_name"] = corrected_food_name

        # Normalize quantity if it's "some"
        if item.get("quantity") == "some":
            item["quantity"] = "1 serving"  # Normalize 'some' to '1 serving'
        
        # Normalize category if not available
        if "category" not in item:
            item["category"] = "unknown"

        # Fetch nutrient data from the API for each food item
        query = f"{item['quantity']} {item['food_name']}"
        nutrient_data = fetch_nutrient_data(query)

        if nutrient_data and "items" in nutrient_data and len(nutrient_data["items"]) > 0:
            # Ensure numerical values are converted to standard Python types
            item["calories"] = int(nutrient_data["items"][0].get("calories", 0)) if not np.isnan(nutrient_data["items"][0].get("calories", 0)) else 0
            item["protein"] = float(nutrient_data["items"][0].get("protein_g", 0))
            item["carbohydrates"] = float(nutrient_data["items"][0].get("carbohydrates_total_g", 0))
            item["fats"] = float(nutrient_data["items"][0].get("fat_total_g", 0))
            item["fiber"] = float(nutrient_data["items"][0].get("fiber_g", 0))
            item["sugars"] = float(nutrient_data["items"][0].get("sugar_g", 0))
        else:
            # Default values if API call fails
            item["calories"] = 0
            item["protein"] = 0
            item["carbohydrates"] = 0
            item["fats"] = 0
            item["fiber"] = 0
            item["sugars"] = 0

    return food_items
