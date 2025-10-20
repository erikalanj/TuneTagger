from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def get_mood_from_text(text: str) -> str:
    """
    Analyzes the sentiment of a given text and returns a corresponding mood
    using a more sophisticated rule-based system.
    """
    sentiment_scores = analyzer.polarity_scores(text)

    compound_score = sentiment_scores["compound"]
    pos_score = sentiment_scores["pos"]
    neg_score = sentiment_scores["neg"]
    neu_score = sentiment_scores["neu"]

    print(f"the compound score of the song is {compound_score}")

    if compound_score >= 1.5:
        return "Exhilarating"
    elif compound_score >= 0.8:
        return "Joyful"
    elif compound_score >= 0.5:
        return "Uplifting"
    elif compound_score > -0.2 and compound_score < 0.2:
        # combination of pos/neg scores and compound score for nuance
        if pos_score > 0.4 and neg_score < 0.1:
            return "Calm"
        elif neg_score > 0.4 and pos_score < 0.1:
            return "Pensive"
        else:
            return "Neutral"
    elif compound_score <= -1.0:
        return "Aggressive"
    elif compound_score <= -0.65:
        return "Somber"
    elif compound_score < -0.4:
        return "Melancholic"

    return "Undetermined"


def analyze_song_mood(description: str, annotations: list[dict]) -> str:
    """
    Combines all available text data for a song and determines its overall mood.

    Args:
        description (str): The main song description.
        annotations (list[dict]): A list of dictionaries containing lyric fragments and annotations.

    Returns:
        str: The determined mood of the song.
    """
    # all text data combined into a single string for analysis
    full_text = description
    for annotation in annotations:
        full_text += " " + annotation.get("lyric_fragment", "")
        full_text += " " + annotation.get("annotation_text", "")

    return get_mood_from_text(full_text)
