import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the Uploaded files into bytes
        bytes = uploaded_file.getvalue()
        image_parts = [{
            "mime_type" : uploaded_file.type,
            "data" : bytes
        }]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
# Streamlit App
st.set_page_config(page_title = "MultiLanguage Invoice Extractor")
st.header("Gemini Application")
input = st.text_input("Input Prompt : ", key = "input")
uploaded_file = st.file_uploader("Choose an Image", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # To Display The Uploaded Image
    st.image(image, caption = "Uploaded Image", use_column_width = True)

submit = st.button("Response")
input_prompt = """
You are an expert in understanding invoices. We upload invoice file or image and you have to answer for any question based on the provided invoices.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is:")
    st.write(response)