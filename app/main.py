from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from testing.genius.genius_req import fetch_song_details, get_genius_access_token

connection = sqlite3.connect("db/tunes.db", check_same_thread=False)
cursor = connection.cursor()

# initlize the database with these columns (if not already there)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
           song_title TEXT NOT NULL,
           song_artist TEXT NOT NULL,
           song_mood TEXT,
           UNIQUE(song_title, song_artist)
       )"""
)

# ADD DOCSTRINGS, THEY LEAVE COMMENTS UNDER YOUR METHODS

connection.commit()


class Song:
    """Song class which defines each entry in the database"""

    def __init__(self, title, artist, mood=None):
        self.title = title
        self.artist = artist
        self.mood = mood

    def get_song_data(self):
        """getter for song data"""
        return (self.title, self.artist, self.mood)


def fetch_database():
    """retrieves all song objects from the database"""
    cursor.execute("SELECT * FROM tunes")
    connection.commit()
    return cursor.fetchall()


def insert_song(song: Song):
    """inserts a song into the tunes database"""
    cursor.execute(
        "INSERT OR IGNORE INTO tunes (song_title, song_artist, song_mood) VALUES (?, ?, ?)",
        song.get_song_data(),
    )
    connection.commit()


def delete_song(title=None, id=None):
    """Deletes a song by id or title from the database"""
    if id is None and title is None:
        return
    if id is not None and title is not None:
        cursor.execute(
            "DELETE FROM tunes WHERE ROWID = ? AND song_title = ?", (id, title)
        )
    elif id is not None:
        cursor.execute("DELETE FROM tunes WHERE ROWID = ?", (id,))
    elif title is not None:
        cursor.execute("DELETE FROM tunes WHERE song_title = ?", (title,))
    connection.commit()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_request():
    data = fetch_database()
    dataframe = pd.DataFrame(data, columns=["Song Title", "Artist Name", "Mood"])

    return render_template("index.html", library_data=dataframe.to_html())


# DELETION BY ID IS NOT WORKING.


@app.route("/post", methods=["POST"])
def post_request():
    title_to_insert = request.form.get("title-to-insert")
    artist_to_insert = request.form.get("artist-to-insert")
    if title_to_insert and artist_to_insert:
        access_token = get_genius_access_token()
        desc, annotations, mood = fetch_song_details(
            title_to_insert, artist_to_insert, access_token
        )
        if mood and mood != "Undetermined":
            new_song = Song(title_to_insert, artist_to_insert, mood)
            insert_song(new_song)
            return redirect(url_for("get_request"))
        # in order to not resubmit on refresh, if you redirect back to the page, it clears forms

    id_to_delete = request.form.get("id-to-delete")
    title_to_delete = request.form.get("title-to-delete")
    if id_to_delete or title_to_delete:
        delete_song(title_to_delete, id_to_delete)
        return redirect(url_for("get_request"))
    # always return a response
    return redirect(url_for("get_request"))


if __name__ == "__main__":
    app.run(debug=True)
