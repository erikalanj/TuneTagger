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
        show_database()


def show_database():
    cursor.execute("SELECT * FROM tunes")


if __name__ == "__main__":
    main()
