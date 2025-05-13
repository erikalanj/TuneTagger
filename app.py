import streamlit as st
import requests
from textblob import TextBlob


st.title("Welcome to TuneTeller")
st.subheader(
    "TuneTeller is a music analysis system that allows you to filter you music by mood, not just genre."
)

song_title = st.text_input("Enter the song title")
artist_name = st.text_input("Enter the artist name")
if st.button("Submit"):
    st.write(f"Song Title: {song_title}")
    st.write(f"Artist Name: {artist_name}")
