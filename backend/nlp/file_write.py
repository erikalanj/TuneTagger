import sys
import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_file_dir)
sys.path.append(parent_dir)

from backend.genius.genius_req import fetch_song_details, get_genius_access_token
from string import Template


def main():
    with open("material.txt", "w") as f:
        song_title = input("Enter title of song you wish to search: ")
        artist_name = input("Enter title of artist for that song: ")

        try:
            print("Fetching song details... Please wait.")
            main_desc, lyric_annotations = fetch_song_details(
                song_title, artist_name, get_genius_access_token()
            )
        except Exception as e:
            print(f"Error fetching song details: {e}")
            return

        if main_desc is None and not lyric_annotations:
            print("No data to write to the file.")
            return
        f.write(
            "Main Description: "
            + (main_desc if main_desc is not None else "No description available")
            + "\n"
        )
        f.write("Lyric Annotations: \n")
        template_lyric = Template("$lyric_fragment: $annotation_text\n")
        for annotation in lyric_annotations:
            if "lyric_fragment" in annotation and "annotation_text" in annotation:
                formatted_lyric = template_lyric.substitute(annotation)
                f.write(formatted_lyric)
            else:
                print(f"Skipping invalid annotation: {annotation}")

    print("File written successfully!")


if __name__ == "__main__":
    main()
