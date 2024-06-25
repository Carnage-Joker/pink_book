import logging
from collections import Counter
from datetime import timedelta
from typing import Tuple

from django.db.models import Avg
from django.db.models.query import QuerySet
from django.utils.timezone import now
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk.tokenize import word_tokenize
logger = logging.getLogger(__name__)


def extract_keywords(entries, num_keywords=10):
    if not entries:
        return []

    text = ' '.join(entry.content for entry in entries)

    if len(text.split()) < num_keywords:
        return []

    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.isalpha(
    ) and word not in stopwords.words('english')]
    most_common = Counter(filtered_tokens).most_common(num_keywords)
    return most_common  # List of tuples (keyword, count)


def get_sentiment(text):
    """
    Analyze the sentiment of the given text using VADER.

    Parameters:
    text (str): The text to be analyzed.

    Returns:
    tuple: A tuple containing the sentiment ('positive', 'negative', 'neutral'),
           polarity (float), and subjectivity (approximate confidence score).
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)

    # Extracting polarity and subjectivity
    # Compound score is a normalized score between -1 and 1
    polarity = sentiment_scores['compound']
    # Approximate confidence score
    subjectivity = (
        sentiment_scores['pos'] + sentiment_scores['neg'] + sentiment_scores['neu']) / 3

    # Determine the sentiment
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment, polarity, subjectivity


# Example usage
try:
    text = "I love this new feature! It's amazing."
    sentiment, polarity, subjectivity = get_sentiment(text)
    print(f"Sentiment: {sentiment}, Polarity: {
          polarity}, Subjectivity: {subjectivity}")
except Exception as e:
    print(f"Error: {e}")



def get_average_sentiment(entries: QuerySet):
    """Calculate the average sentiment of queryset entries."""
    if not entries.exists():
        return {'avg_polarity': None, 'avg_subjectivity': None}

    return {
        'avg_polarity': entries.aggregate(Avg('polarity'))['polarity__avg'],
        'avg_subjectivity': entries.aggregate(Avg('subjectivity'))['subjectivity__avg']
    }


def get_most_common_tags(entries):
    tags = [tag.name for entry in entries for tag in entry.tags.all()]
    return Counter(tags).most_common(1)


def get_most_common_emotions(entries):
    emotions = [entry.sentiment for entry in entries if entry.sentiment]
    return Counter(emotions).most_common(1)


def get_current_streak(entries):
    if not entries:
        return 0

    streak = 0
    current_date = now().date()

    for entry in entries:
        if entry.timestamp.date() == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    return streak


def get_average_word_count(entries):
    if not entries:
        return 0

    total_words = sum(len(entry.content.split()) for entry in entries)
    return total_words // len(entries)


def get_peak_journaling_time(entries):
    if not entries:
        return None

    hours = [entry.timestamp.hour for entry in entries]
    most_common_hour = Counter(hours).most_common(1)
    return most_common_hour[0][0] if most_common_hour else None
