import streamlit as st
import sqlite3

connection = sqlite3.connect("tunes.db")
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
               song_title TEXT NOT NULL,
               song_artist TEXT NOT NULL
               )"""
)

connection.commit()


def main():
    st.title("Welcome to TuneTeller")
    st.subheader(
        "TuneTeller is a music analysis system that allows you to filter you music by mood, not just genre."
    )
    song_title = st.text_input("Enter the song title")
    song_artist = st.text_input("Enter the artist name")
    if st.button("Submit"):
        st.write(f"Song Title: {song_title}")
        st.write(f"Artist Name: {song_artist}")
        cursor.execute(
            "INSERT INTO tunes (song_title, song_artist) VALUES (?, ?)",
            (song_title, song_artist),
        )
        connection.commit()
    if st.button("Show all songs!"):
        st.write(show_database())
        connection.commit()


def show_database():
    cursor.execute("SELECT * FROM tunes")
    return cursor.fetchall()


if __name__ == "__main__":
    main()
