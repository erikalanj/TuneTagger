from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd

connection = sqlite3.connect("db/tunes.db", check_same_thread=False)
cursor = connection.cursor()

# initlize the database with these columns (if not already there)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
           song_title TEXT NOT NULL,
           song_artist TEXT NOT NULL,
           UNIQUE(song_title, song_artist)
       )"""
)

connection.commit()


class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def get_song_data(self):
        return (self.title, self.artist)


def fetch_database():
    cursor.execute("SELECT * FROM tunes")
    return cursor.fetchall()


def insert_song(song: Song):
    cursor.execute(
        "INSERT OR IGNORE INTO tunes (song_title, song_artist) VALUES (?, ?)",
        song.get_song_data(),
    )


app = Flask(__name__)


@app.route("/index", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        title = request.form["title-to-insert"]
        artist = request.form["artist-to-insert"]
        if title and artist:
            new_song = Song(title, artist)
            insert_song(new_song)
            connection.commit()
            # in order to not resubmit on refresh, if you redirect back to the page, it clears forms
            return redirect(url_for("index"))

    data = fetch_database()
    dataframe = pd.DataFrame(data, columns=["Song Title", "Artist Name"])
    connection.commit()
    return render_template("index.html", library_data=dataframe.to_html())


if __name__ == "__main__":
    app.run(debug=True)
