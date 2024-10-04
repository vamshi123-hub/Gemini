import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response = chat.send_message(question, stream = True)
    return response
##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini Application")

#Initialize Session State For Chat History if it does not exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input=st.text_input("Input: ",key="input")
submit = st.button("Ask questions")

if submit and input:
    response = get_gemini_response(input)
    #Add a Query and Response to Session Chat History
    st.session_state["chat_history"].append(("You", input))
    st.subheader("The Response is:")
    for chunks in response:
        st.write(chunks.text)
        st.session_state["chat_history"].append(("Chatbot", chunks.text))

st.subheader("The Chat Hitory is:")

for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")

