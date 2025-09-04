from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from backend.genius.genius_req import fetch_song_details, get_genius_access_token

connection = sqlite3.connect("db/tunes.db", check_same_thread=False)

cursor = connection.cursor()

# Updated: Added a primary key 'id' column to the table.
cursor.execute(
    """CREATE TABLE IF NOT EXISTS tunes(
           id INTEGER PRIMARY KEY,
           song_title TEXT NOT NULL,
           song_artist TEXT NOT NULL,
           song_mood TEXT,
           UNIQUE(song_title, song_artist)
       )"""
)

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
    """Retrieves all song objects from the database, including their ID."""
    # Updated: Select the 'id' column.
    cursor.execute("SELECT id, song_title, song_artist, song_mood FROM tunes")
    connection.commit()
    return cursor.fetchall()


def insert_song(song: Song):
    """inserts a song into the tunes database"""
    # Updated: Let the 'id' column autoincrement by not including it in the insert statement.
    cursor.execute(
        "INSERT OR IGNORE INTO tunes (song_title, song_artist, song_mood) VALUES (?, ?, ?)",
        song.get_song_data(),
    )
    connection.commit()


def delete_song(id=None):
    """Deletes a song by id from the database"""
    if id is not None:
        # Fixed: Cast the ID to an integer for the database query.
        try:
            int_id = int(id)
            cursor.execute("DELETE FROM tunes WHERE id = ?", (int_id,))
            connection.commit()
        except (ValueError, TypeError):
            # This handles cases where the form data isn't a valid integer
            pass


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_request():
    data = fetch_database()
    # Updated: Include 'ID' in the DataFrame columns to match the database query.
    dataframe = pd.DataFrame(data, columns=["ID", "Song Title", "Artist Name", "Mood"])

    dataframe.insert(0, "#", range(1, 1 + len(dataframe)))

    # Pass the entire DataFrame to the template, not just the HTML.
    return render_template("index.html", library_data=dataframe)


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

    id_to_delete = request.form.get("id-to-delete")
    if id_to_delete:
        # The delete_song function now handles the integer casting.
        delete_song(id_to_delete)
        return redirect(url_for("get_request"))

    return redirect(url_for("get_request"))


if __name__ == "__main__":
    app.run(debug=True)
