import numpy as np
from PIL import Image
import requests

# USDA API Configuration
API_KEY = "mxfs0mxIPBQTPctU4ck9typTSwmXHLTlrAnfDFzu"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def preprocess_image(image: Image.Image):
    """Resize and normalize image for model input"""
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def fetch_nutrition_data(food_name):
    """Fetch calories, protein, fat, and carbs from USDA API"""
    params = {"query": food_name, "api_key": API_KEY}
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "foods" in data and len(data["foods"]) > 0:
            nutrients = data["foods"][0]["foodNutrients"]
            nutrition_info = {
                "calories": next((n["value"] for n in nutrients if n["nutrientName"] == "Energy"), "Unknown"),
                "protein": next((n["value"] for n in nutrients if n["nutrientName"] == "Protein"), "Unknown"),
                "fat": next((n["value"] for n in nutrients if n["nutrientName"] == "Total lipid (fat)"), "Unknown"),
                "carbohydrates": next((n["value"] for n in nutrients if n["nutrientName"] == "Carbohydrate, by difference"), "Unknown")
            }
            return nutrition_info

    return {"calories": "Unknown", "protein": "Unknown", "fat": "Unknown", "carbohydrates": "Unknown"}