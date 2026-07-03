"""
Sentiment analysis helper functions using TextBlob.
"""
from textblob import TextBlob
import pandas as pd


def get_sentiment_scores(text: str):
    """
    Returns polarity (-1 to 1) and subjectivity (0 to 1) for a piece of text.
    """
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity


def classify_sentiment(polarity: float) -> str:
    """
    Classifies a polarity score into Positive / Neutral / Negative.
    """
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


def analyze_dataframe(df: pd.DataFrame, text_column: str = "Customer Review") -> pd.DataFrame:
    """
    Adds Polarity, Subjectivity, and Sentiment columns to a dataframe
    based on the given text column.
    """
    df = df.copy()
    scores = df[text_column].apply(get_sentiment_scores)
    df["Polarity"] = scores.apply(lambda x: x[0])
    df["Subjectivity"] = scores.apply(lambda x: x[1])
    df["Sentiment"] = df["Polarity"].apply(classify_sentiment)
    return df
