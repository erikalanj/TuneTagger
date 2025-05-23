import streamlit as st
import sqlite3
import pandas as pd


connection = sqlite3.connect("tunes.db")
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
               song_title TEXT NOT NULL,
               song_artist TEXT NOT NULL
               )"""
)

connection.commit()

# class Song:
#     def __init__ (self, song_title, song_artist):
#         self.song_title = song_title
#         self.song_artist = song_artist


def show_database():
    cursor.execute("SELECT * FROM tunes")
    return cursor.fetchall()


def insert_song(song_title, song_artist):
    cursor.execute(
        "INSERT INTO tunes (song_title, song_artist) VALUES (?, ?)",
        (song_title, song_artist),
    )


if __name__ == "__main__":
    # Centered title and subtitle
    st.title("Welcome to TuneTagger")

    st.subheader("Enter any song you want and create a library")

    st.write("")  # Adds a little vertical space

    song_title = st.text_input("Enter the song title")
    song_artist = st.text_input("Enter the artist name")

    if st.button("Submit") and song_title and song_artist:
        st.write(f"Added {song_title} by {song_artist} to your library")
        insert_song(song_title, song_artist)
        connection.commit()

    if st.toggle("View library"):
        data = show_database()
        dataframe = pd.DataFrame(data, columns=["Song Title", "Artist Name"])
        st.table(dataframe)
        connection.commit()
