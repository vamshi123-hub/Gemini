import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import sqlite3

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(question, prompt):
    result = model.generate_content([prompt[0], question])
    response = result.text.strip()
    return response

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt = ["""
    You are an expert in converting English questions to SQL query, focusing on generating the SQL query itself without additional explanations like 'Okay'.
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION and MARKS \n\nFor example, \nExample 1 - How many entries of records are present 
    the SQL command will be something like this SELECT COUNT (*) FROM STUDENT ; 
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science";
    also the sql code should not have in beginning or end and sql word in output
"""]

st.set_page_config(page_title = "Retrieve SQL query")
st.header("Gemini App To Retrieve SQL Data")
question = st.text_input("Input:", key = "input")
submit = st.button("Ask Questions ?")

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response, "Student.db")
    st.subheader("The Response is:")
    for row in data:
        print(row)
        st.subheader(row)

