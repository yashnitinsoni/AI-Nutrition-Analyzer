import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://127.0.0.1:8000/predict"

st.title("🍏 AI Nutrition Assistant")
st.subheader("Upload an image of your food and get its nutritional value!")

uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
    response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        result = response.json()
        st.subheader(f"🍽️ Food Detected: {result['food'].title()}")
        st.write(f"**Calories:** {result['calories']} kcal")
        st.write(f"**Protein:** {result['protein']} g")
        st.write(f"**Fat:** {result['fat']} g")
        st.write(f"**Carbohydrates:** {result['carbohydrates']} g")
    else:
        st.error("⚠️ Error processing the image.")