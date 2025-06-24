import pandas as pd
import lyricsgenius
import os
import csv
import time

# --- Configuration ---
# It's highly recommended to use environment variables for tokens in a real app.
# client_access_token = os.environ.get("GENIUS_ACCESS_TOKEN")
client_access_token = "aa4ZOA-5Fm6597GmdwfLLgBfePglT6pEk1-U-NThxM0GGw45h_t531LB7IiPH7pD"

if not client_access_token:
    raise ValueError(
        "GENIUS_ACCESS_TOKEN not found. Please set it as an environment variable."
    )

genius = lyricsgenius.Genius(
    client_access_token,
    remove_section_headers=True,
    skip_non_songs=True,
    verbose=False,  # Set to False to reduce console output from lyricsgenius
)

artist = "Sia"
nb_songs = 1  # Fetching only one song for testing purposes

titles = []
descriptions = []


# --- DOM Extraction Function ---
def extract_text_from_genius_dom(dom_data):
    """
    Recursively extract text from Genius API's 'dom' structure within a description.
    Handles various nested structures including 'plain' text, lists, and dictionaries with 'children'.
    """
    if isinstance(dom_data, str):
        return dom_data
    elif isinstance(dom_data, dict):
        # Prioritize 'plain' text if available, as it's often the most direct.
        if "plain" in dom_data and dom_data["plain"]:
            return dom_data["plain"]

        # If not 'plain', then process 'dom' structure by looking for 'children'.
        children = dom_data.get("children", [])
        return "".join(extract_text_from_genius_dom(child) for child in children)
    elif isinstance(dom_data, list):
        return "".join(extract_text_from_genius_dom(child) for child in dom_data)
    return ""


# --- Main Logic ---
print(f"Searching for songs by {artist}...")
artist_genius = genius.search_artist(artist, max_songs=nb_songs, sort="popularity")

songs = []
if artist_genius is not None:
    songs = artist_genius.songs
    print(f"Found {len(songs)} songs for {artist}.")
else:
    print(f"No artist found with the name '{artist}'.")

for (
    song_item
) in songs:  # Renamed loop variable to avoid conflict with `genius.song` method
    if song_item is not None:
        titles.append(song_item.title)
        print(f"Processing song: {song_item.title}")

        desc_text = "No description available."  # Default fallback

        try:
            # OPTION 1: Try to get the description directly from the lyricsgenius Song object.
            # This is often the simplest if lyricsgenius handles it.
            # full_song_obj = genius.song(song_item.id) # This gives a Song object directly

            # OPTION 2: Fetch raw JSON to access the 'description' field's 'dom' or 'plain' data.
            # This is more robust as it guarantees access to the underlying API structure.
            raw_song_info = genius.song(song_item.id)

            if (
                isinstance(raw_song_info, dict)
                and "response" in raw_song_info
                and "song" in raw_song_info["response"]
            ):
                song_data = raw_song_info["response"]["song"]
                description_data = song_data.get(
                    "description"
                )  # This will be the complex rich_text_object

                if description_data:  # Check if description_data exists
                    # Try to get the plain text first if available, otherwise parse the DOM
                    if isinstance(description_data, dict):
                        if "plain" in description_data and description_data["plain"]:
                            desc_text = description_data["plain"]
                        elif "dom" in description_data:
                            desc_text = extract_text_from_genius_dom(
                                description_data["dom"]
                            )
                    elif isinstance(
                        description_data, str
                    ):  # Handle cases where it's a direct string
                        desc_text = description_data

                # Further fallback for very short/invalid descriptions that might be URLs
                if not desc_text or "https://docs.genius.com" in desc_text:
                    desc_text = "No detailed description available."

            else:
                print(f"Warning: Could not retrieve full info for {song_item.title}.")

        except Exception as e:
            print(
                f"Error fetching description for {song_item.title} (ID: {song_item.id}): {e}"
            )
            desc_text = "Error fetching description."

        descriptions.append(
            desc_text.strip()
        )  # .strip() to clean up leading/trailing whitespace

# Create DataFrame
data = pd.DataFrame({"artist": artist, "title": titles, "description": descriptions})

print("\n--- Results ---")
print(data)
