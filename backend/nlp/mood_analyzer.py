from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def get_mood_from_text(text: str) -> str:
    """
    Analyzes the sentiment of a given text and returns a corresponding mood.

    Args:
        text (str): The combined string of song lyrics, descriptions, and annotations.

    Returns:
        str: A string representing the mood (e.g., 'Uplifting', 'Somber', 'Neutral').
    """
    # Use VADER to get the sentiment scores for the text
    sentiment_scores = analyzer.polarity_scores(text)

    # The compound score is the most useful for overall sentiment
    compound_score = sentiment_scores["compound"]

    # Map the compound score to a specific mood
    if compound_score >= 0.2:
        return "Uplifting"
    elif compound_score > -0.2 and compound_score < 0.2:
        return "Neutral"
    else:
        return "Somber"


def analyze_song_mood(description: str, annotations: list[dict]) -> str:
    """
    Combines all available text data for a song and determines its overall mood.

    Args:
        description (str): The main song description.
        annotations (list[dict]): A list of dictionaries containing lyric fragments and annotations.

    Returns:
        str: The determined mood of the song.
    """
    # Combine all text data into a single string for analysis
    full_text = description
    for annotation in annotations:
        full_text += " " + annotation.get("lyric_fragment", "")
        full_text += " " + annotation.get("annotation_text", "")

    return get_mood_from_text(full_text)
