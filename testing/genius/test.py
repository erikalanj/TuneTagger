# the description, as well as the lyric annotations are succesfully retrieved by this script
# the descipriont is just stored as a string, and the lyric annotations as a list of dictionaries
# the lyric annotations have lyric_fragment and annotation_text as keys in each element, with each key having its own text value


import requests
import os
import json
import traceback  # Import traceback for detailed error logging

# --- Configuration ---
# It's highly recommended to use environment variables for tokens in a real app.
# For demonstration, we are using a hardcoded token.
# client_access_token = os.getenv("GENIUS_ACCESS_TOKEN")
client_access_token = "aa4ZOA-5Fm6597GmdwfLLgBfePglT6pEk1-U-NThxM0GGw45h_t531LB7IiPH7pD"

# Ensure the token is set, even if hardcoded for testing
if not client_access_token:
    print(
        "Error: GENIUS_ACCESS_TOKEN environment variable not set, and no hardcoded token found."
    )
    print("Please set it or provide it directly in the script for testing.")
    exit()


def get_genius_access_token():
    """
    Retrieves the Genius API client access token.
    In this modified version, it returns the hardcoded token or the environment variable one.
    """
    return client_access_token


def search_song(song_title, artist_name, access_token):
    url = f"https://api.genius.com/search?q={song_title} {artist_name}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print("Request URL:", url)  # Debugging
    print("Response Status Code:", response.status_code)  # Debugging
    print("Response JSON:", response.json())  # Debugging
    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        for hit in hits:
            if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
                return hit["result"]["id"]
    return None


def fetch_song_details(song_title, artist_name, access_token):
    song_id = search_song(song_title, artist_name, access_token)

    if song_id:
        print(f"Found song ID: {song_id}. Fetching descriptions and annotations...")
        main_desc, lyric_annotations = get_song_details_and_annotations(
            song_id, access_token
        )

        # Print Main Song Description
        print("\n--- Main Song Description ---")
        print(main_desc)

        # Print Lyric Annotations
        print("\n--- Lyric Annotations ---")
        if lyric_annotations:
            for i, anno_pair in enumerate(lyric_annotations):
                print(
                    f"\n--- Lyric Annotation {i+1} for: '{anno_pair['lyric_fragment']}' ---"
                )
                print(anno_pair["annotation_text"])
            print("\n------------------------------------")
        else:
            print("No specific lyric annotations found for this song.")

        return main_desc, lyric_annotations
    else:
        print("Song not found.")
        return None, None
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        for hit in data["response"]["hits"]:
            if hit["type"] == "song":
                song_id = hit["result"]["id"]
                return song_id
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during song search: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for search: {e}")
        # print(f"Problematic response content: {response.text}") # Uncomment for deeper debugging
        traceback.print_exc()  # Print full traceback for debugging
        return None


def extract_text_from_dom(dom_element):
    """
    Recursively extracts plain text from a Genius API DOM structure.
    Handles various nested structures including 'plain' text, lists, and dictionaries with 'children'.
    Also handles line breaks.
    """
    text_content = []
    if isinstance(dom_element, dict):
        if (
            "plain" in dom_element and dom_element["plain"]
        ):  # Prefer 'plain' if available
            text_content.append(dom_element["plain"])
        elif "children" in dom_element:
            for child in dom_element["children"]:
                text_content.append(extract_text_from_dom(child))
        elif dom_element.get("tag") == "br":
            text_content.append("\n")  # Handle line breaks
    elif isinstance(dom_element, str):
        text_content.append(dom_element)

    return "".join(text_content)


def get_song_details_and_annotations(song_id, access_token):
    """
    Fetches the main song description and then lyric-specific annotations.
    Returns a tuple: (main_description_text, list_of_lyric_annotations_text).
    """
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {access_token}"}

    main_description_text = "No detailed song description available."
    lyric_annotations_list = []

    # --- 1. Fetch Main Song Description (from /songs endpoint) ---
    song_url = f"{base_url}/songs/{song_id}"
    try:
        response = requests.get(song_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "response" in data and "song" in data["response"]:
            song_data = data["response"]["song"]
            if "description" in song_data and "dom" in song_data["description"]:
                extracted_desc = extract_text_from_dom(
                    song_data["description"]["dom"]
                ).strip()
                if extracted_desc:
                    main_description_text = extracted_desc
            elif (
                "description" in song_data
                and "plain" in song_data["description"]
                and song_data["description"]["plain"]
            ):
                # Fallback to plain if available, though extract_text_from_dom should cover this
                main_description_text = song_data["description"]["plain"].strip()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching main song description from /songs endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for main description: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        # print(f"Problematic response content for song details: {response.text}") # Uncomment for deeper debugging

    # --- 2. Fetch Lyric Annotations (from /referents endpoint) ---
    referents_url = f"{base_url}/referents"
    referents_params = {"song_id": song_id}

    try:
        response = requests.get(referents_url, headers=headers, params=referents_params)
        response.raise_for_status()
        data = response.json()

        # print(json.dumps(data, indent=2)) # Uncomment this to inspect referents response!

        if "response" in data and "referents" in data["response"]:
            for referent in data["response"]["referents"]:
                # A referent can be a lyric line that has an annotation
                # The annotation body is usually within the 'annotations' list inside the referent.
                if "annotations" in referent:
                    for annotation in referent["annotations"]:
                        if "body" in annotation and "dom" in annotation["body"]:
                            lyric_annotation_text = extract_text_from_dom(
                                annotation["body"]["dom"]
                            ).strip()

                            # Also try to get the fragment (the lyric text itself) that the annotation refers to
                            fragment = referent.get("fragment", "N/A").strip()

                            if lyric_annotation_text:
                                # Store as a dictionary to keep lyric fragment and annotation text together
                                lyric_annotations_list.append(
                                    {
                                        "lyric_fragment": fragment,
                                        "annotation_text": lyric_annotation_text,
                                    }
                                )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching lyric annotations from /referents endpoint: {e}")
        traceback.print_exc()  # Print full traceback for debugging
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for lyric annotations: {e}")
        traceback.print_exc()  # Print full traceback for debugging
        # print(f"Problematic response content for referents: {response.text}") # Uncomment for deeper debugging

    return main_description_text, lyric_annotations_list


def main():
    """
    Main function to prompt user for song and artist and print descriptions and annotations.
    """
    access_token = get_genius_access_token()

    song_title = input("Enter the song title: ")
    artist_name = input("Enter the artist name: ")

    print(f"\nSearching for '{song_title}' by '{artist_name}'...")
    song_id = search_song(song_title, artist_name, access_token)

    if song_id:
        print(f"Found song ID: {song_id}. Fetching descriptions and annotations...")
        main_desc, lyric_annotations = get_song_details_and_annotations(
            song_id, access_token
        )

        # Print Main Song Description
        print("\n--- Main Song Description ---")
        print(main_desc)

        # Print Lyric Annotations
        print("\n--- Lyric Annotations ---")
        if lyric_annotations:
            for i, anno_pair in enumerate(lyric_annotations):
                print(
                    f"\n--- Lyric Annotation {i+1} for: '{anno_pair['lyric_fragment']}' ---"
                )
                print(anno_pair["annotation_text"])
            print("\n------------------------------------")
        else:
            print("No specific lyric annotations found for this song.")
            print(
                "It's possible there are no public lyric annotations available via the API for this song."
            )
    else:
        print(
            f"Could not find '{song_title}' by '{artist_name}'. Please check the spelling."
        )


if __name__ == "__main__":
    main()
