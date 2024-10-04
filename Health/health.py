import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import streamlit as st
from PIL import Image
#import base64

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
#model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        #base64_encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        image_parts = [{
            "mime_type" : uploaded_file.type,
            "data" : bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


st.set_page_config(page_title = "Calories Calculations")
st.header("Calories Calculations Using Gemini ✨")
#input = st.text_input("Input Prompt: ", key = "input")
uploaded_file = st.file_uploader("Choose an Image", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image", use_column_width = True)

submit = st.button("Tell me about the total calories")

input_prompt = """
    You are an expert in nutritionist where the you need to see the food items from the uploaded image 
    and calculate the total calories, also provide the details of every food items with calories intake 
    in below format
    1. Item 1 - no of calories
    2. Item 2 - no of calories
    - - - -
    - - - -

    Finally you can also mention whether the food is healthy or not and also mention the
    percentage split of the ratio of carbohydrates, fats, fibers, sugar and other important
    things required in our diet
        
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The Response is:")
    st.write(response)