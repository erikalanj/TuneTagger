import sys
import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_file_dir)
sys.path.append(parent_dir)

from testing.genius.genius_req import fetch_song_details, get_genius_access_token
from string import Template


def main():
    with open("material.txt", "w") as f:
        song_title = input("Enter title of song you wish to search: ")
        artist_name = input("Etner title of artist for that song: ")

        main_desc, lyric_annotations = fetch_song_details(
            song_title, artist_name, get_genius_access_token()
        )
        print("Attempted to write to file")
        f.write(
            "Main Description: "
            + (main_desc if main_desc is not None else "No description available")
            + "\n"
        )
        f.write("Lyric Annotations: \n")
        template_lyric = Template("$lyric_fragment: $annotation_text\n")
        for i in range(len(lyric_annotations) if lyric_annotations is not None else 0):
            if lyric_annotations is not None:
                formatted_lyric = template_lyric.substitute(lyric_annotations[i])
                f.write(formatted_lyric)


if __name__ == "__main__":
    main()
