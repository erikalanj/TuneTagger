from flask import Flask, render_template, request, redirect, url_for, jsonify
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


def query_all_songs(sort_by_mood=False):
    """Queries all songs from the database.
    Returns list of tuples: (id, title, artist, mood)
    """
    query = "SELECT id, song_title, song_artist, song_MOOD FROM tunes"
    if sort_by_mood:
        query += "ORDER BY song_mood ASC"
    cursor.execute(query)
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
def index():
    """Main page route - displays the song library"""
    data = query_all_songs()
    # Updated: Include 'ID' in the DataFrame columns to match the database query.
    dataframe = pd.DataFrame(data, columns=["ID", "Song Title", "Artist Name", "Mood"])

    dataframe.insert(0, "#", range(1, 1 + len(dataframe)))

    # Pass the entire DataFrame to the template, not just the HTML.
    return render_template("index.html", library_data=dataframe)


@app.route("/api/add-song", methods=["POST"])
def api_add_song():
    """AJAX endpoint for adding a song"""
    title = request.form.get("title-to-insert")
    artist = request.form.get("artist-to-insert")

    if not title or not artist:
        return (
            jsonify({"success": False, "error": "Title and artist are required"}),
            400,
        )

    access_token = get_genius_access_token()
    desc, annotations, mood = fetch_song_details(title, artist, access_token)

    if mood and mood != "Undetermined":
        new_song = Song(title, artist, mood)
        insert_song(new_song)
        return jsonify(
            {
                "success": True,
                "song": {"title": title, "artist": artist, "mood": mood},
                "library": format_songs_for_json(),
            }
        )
    else:
        return (
            jsonify(
                {"success": False, "error": "Could not determine mood for this song"}
            ),
            400,
        )


@app.route("/api/delete-song", methods=["POST"])
def api_delete_song():
    """AJAX endpoint for deleting a song"""
    song_id = request.form.get("id-to-delete")

    if not song_id:
        return jsonify({"success": False, "error": "Song ID is required"}), 400

    delete_song(song_id)
    return jsonify({"success": True, "library": format_songs_for_json()})


def format_songs_for_json():
    """Formats song data as a list of dicts for JSON/AJAX responses"""
    data = query_all_songs()
    library = []
    for idx, row in enumerate(data, 1):
        library.append(
            {
                "num": idx,
                "id": row[0],
                "title": row[1],
                "artist": row[2],
                "mood": row[3],
            }
        )
    return library


if __name__ == "__main__":
    app.run(debug=True)
