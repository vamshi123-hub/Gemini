import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini Application")
input=st.text_input("Input: ",key="input")
submit = st.button("Ask questions")

if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is:")
    st.write(response)
