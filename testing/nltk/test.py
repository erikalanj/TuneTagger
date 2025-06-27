import sys
import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_file_dir)
sys.path.append(parent_dir)

from genius.test import fetch_song_details, get_genius_access_token


def main():
    with open("material.txt", "w") as f:
        song_title = input("Enter title of song you wish to search: ")
        artist_name = input("Etner title of artist for that song: ")

        main_desc, lyric_annotations = fetch_song_details(
            song_title, artist_name, get_genius_access_token()
        )

        f.write(
            "Main Description: "
            + (main_desc if main_desc is not None else "No description available")
            + "\n"
        )
        f.write("Lyric Annotations: ")
        for i in range(len(lyric_annotations) if lyric_annotations is not None else 0):
            if lyric_annotations is not None:
                f.write(str(lyric_annotations[i].items()))


if __name__ == "__main__":
    main()
