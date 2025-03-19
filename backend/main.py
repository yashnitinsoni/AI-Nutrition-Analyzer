import uvicorn
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np
from backend.utils import preprocess_image, fetch_nutrition_data
from backend.model import predict_food

app = FastAPI()

@app.post("/predict")
async def predict_food_endpoint(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    processed_image = preprocess_image(image)

    # Get Prediction from Fine-Tuned Model
    food_name = predict_food(processed_image)

    # Fetch Nutrition Data from USDA API
    nutrition_info = fetch_nutrition_data(food_name)

    return {"food": food_name, **nutrition_info}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)