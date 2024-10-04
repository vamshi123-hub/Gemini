from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
    You are youtube video summarizer.
    you will be taking the transcript text and summarizing the entire video and 
    providing the detailed summary of 400 words.
    Please provide the summary of the text gievn here: 
"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " "+i["text"]
        return transcript
    except Exception as e:
        raise e

# Getting Summary Based on Prompt
def generate_gemini_content(transcript_text, prompt):
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript Using Gemini ✨")
#st.header("YouTube Transcript Using Gemini ✨")
Youtube_link = st.text_input("Enter YouTube Link")
if Youtube_link:
    video_id = Youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width = True)
submit = st.button("Transcript")

if submit:
    transcript_text = extract_transcript_details(Youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("Detailed Notes")
        st.write(summary)
