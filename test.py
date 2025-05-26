from flask import Flask, render_template
import sqlite3
import pandas as pd

connection = sqlite3.connect("tunes.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
               song_title TEXT NOT NULL,
               song_artist TEXT NOT NULL
               )"""
)

connection.commit()


def show_database():
    cursor.execute("SELECT * FROM tunes")
    return cursor.fetchall()


def insert_song(song_title, song_artist):
    cursor.execute(
        "INSERT INTO tunes (song_title, song_artist) VALUES (?, ?)",
        (song_title, song_artist),
    )


app = Flask(__name__)


@app.route("/")
def index():
    data = show_database()
    dataframe = pd.DataFrame(data, columns=["Song Title", "Artist Name"])
    connection.commit()
    return render_template("index.html", library_data=dataframe.to_html())


if __name__ == "__main__":
    app.run(debug=True)
