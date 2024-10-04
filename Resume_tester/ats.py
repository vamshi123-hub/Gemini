import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import streamlit as st
from PIL import Image
import pdf2image
import base64
import io
import base64

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, pdf_content, prompt):
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #Convert pdf into image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        #Conert into bytes
        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format = "JPEG")
        img_bytes_arr = img_bytes_arr.getvalue()
        pdf_parts = [{
            "mime_type" : "image/jpeg",
            "data" : base64.b64encode(img_bytes_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Exists")
    
st.set_page_config(page_title = "ATS")
st.header("ATS Resume Expert")
input_text = st.text_area("Job description:", key = "input")
uploaded_file = st.file_uploader("Upload a File", type = ["pdf"])
if uploaded_file is not None:
    st.write("Pdf Uploded Successfully")

submit_1 = st.button("Tell me about the Resume")

#submit_2 = st.button("How Can I Improvise My Skils")

submit_3 = st.button("Percentage Match")

input_prompt_1 = """
You are an experienced HR With Tech Experience in the field of any one job role from Data Science, Full Stack,
Web development, Big Data Engineering, DEVOPS,Data Analyst, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt_3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science, Web development,Full Stack,
Big Data Engineering, DEVOPS,Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches 
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit_1:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt_1, pdf_content, input_text)
    st.subheader("The Response is:")
    st.write(response)

if submit_3:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt_3, pdf_content, input_text)
    st.subheader("The Response is:")
    st.write(response)