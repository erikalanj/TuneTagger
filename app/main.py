from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import pandas as pd
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from backend.genius.genius_req import fetch_song_details, get_genius_access_token

MOOD_ORDER = [
    "Exhilarating",
    "Joyful",
    "Uplifting",
    "Calm",
    "Neutral",
    "Pensive",
    "Melancholic",
    "Somber",
    "Aggressive",
    "Undetermined",
]

connection = sqlite3.connect("db/tunes.db", check_same_thread=False)

cursor = connection.cursor()

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


def get_available_moods():
    """Retrieves unique, non-null mood names in database"""
    cursor.execute("SELECT DISTINCT song_mood FROM tunes WHERE song_mood IS NOT NULL")
    all_moods = [row[0] for row in cursor.fetchall()]
    return all_moods


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
    cursor.execute(
        "INSERT OR IGNORE INTO tunes (song_title, song_artist, song_mood) VALUES (?, ?, ?)",
        song.get_song_data(),
    )
    connection.commit()


def delete_song(id=None):
    """Deletes a song by id from the database"""
    if id is not None:
        try:
            int_id = int(id)
            cursor.execute("DELETE FROM tunes WHERE id = ?", (int_id,))
            connection.commit()
        except (ValueError, TypeError):  # handles where input is not valid integer
            pass


app = Flask(__name__)


@app.route("/", methods=["GET"])
# def get_request():
#     sort_mood = (
#         request.args.get("sort") == "mood"
#     )  # check if sort paramater is in query

#     selected_moods = request.args.getlist("filter_moods")
#     selected_moods = [m for m in selected_moods if m]


#     data = query_all_songs(sort_by_mood=sort_mood)
#     available_moods = get_available_moods()
def index():
    """Main page route - displays the song library"""
    # Updated: Include 'ID' in the DataFrame columns to match the database query.
    sort_mood = (
        request.args.get("sort") == "mood"
    )  # check if sort paramater is in query

    selected_moods = request.args.getlist("filter_moods")
    selected_moods = [m for m in selected_moods if m]
    data = query_all_songs(sort_by_mood=sort_mood)
    available_moods = get_available_moods()
    dataframe = pd.DataFrame(data, columns=["ID", "Song Title", "Artist Name", "Mood"])

    if selected_moods:
        dataframe = dataframe[dataframe["Mood"].isin(selected_moods)]

    dataframe.insert(0, "#", range(1, 1 + len(dataframe)))

    return render_template(
        "index.html",
        library_data=dataframe,
        is_sorted_by_mood=sort_mood,
        available_moods=available_moods,
        selected_moods=selected_moods,
    )


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

    id_to_delete = request.form.get("id-to-delete")
    if id_to_delete:
        delete_song(id_to_delete)
        return redirect(url_for("get_request"))
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
