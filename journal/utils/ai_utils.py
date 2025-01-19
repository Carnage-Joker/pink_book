import logging
from collections import Counter
from datetime import timedelta

from django.db.models import Avg, Count, F, IntegerField, Sum, Value
from django.db.models.functions import ExtractHour, Length
from django.db.models.query import QuerySet
from django.utils.timezone import now
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)

NO_DATA_AVAILABLE = 'No data available'


def get_dashboard_insights(entries, habits, todos):
    """Collect all insights for the user's dashboard."""
    if not entries.exists():
        return {
            'habit_consistency': 0,
            'weekly_reflection_count': 0,
            'chores_completed': 0,
            'avg_sentiment': NO_DATA_AVAILABLE,
            'most_common_tags': NO_DATA_AVAILABLE,
            'current_streak': 0,
            'peak_journaling_time': NO_DATA_AVAILABLE,
        }

    avg_sentiment_score = entries.aggregate(Avg('polarity'))['polarity__avg']
    avg_sentiment = (
        'positive' if avg_sentiment_score > 0 else
        'negative' if avg_sentiment_score < 0 else
        'neutral'
    ) if avg_sentiment_score is not None else NO_DATA_AVAILABLE

    return {
        'habit_consistency': get_habit_consistency(habits),
        'weekly_reflection_count': get_weekly_reflection_count(entries),
        'chores_completed': get_chores_completed(todos),
        'avg_sentiment': avg_sentiment,
        'most_common_tags': get_most_common_tags(entries),
        'current_streak': get_current_streak(entries),
        'peak_journaling_time': get_peak_journaling_time(entries),
    }


def get_most_common_tags(entries: QuerySet) -> str:
    """Get the most common tags from entries."""
    from django.db.models import Count
    
    tag_counts = entries.values('tags__name').annotate(tag_count=Count('tags__name')).order_by('-tag_count')
    return tag_counts[0]['tags__name'] if tag_counts else NO_DATA_AVAILABLE

def get_habit_consistency(habits):
    """Calculate habit consistency as a percentage."""
    if not habits.exists():
        return 0
    habit_streaks = [
        habit.increment_counter
        for habit in habits
        if hasattr(habit, 'increment_counter')
    ]
    return round(sum(habit_streaks) / len(habit_streaks) * 100) if habit_streaks else 0


def get_weekly_reflection_count(entries):
    """Calculate the number of reflections made in the past week."""
    one_week_ago = now() - timedelta(days=7)
    return entries.filter(timestamp__gte=one_week_ago).count()


def get_chores_completed(todos: QuerySet) -> int:
    """Calculate the number of chores completed."""
    return todo.filter(task_type='chore', completed=True).count()

    def get_most_common_tags(entries: QuerySet) -> str:
        """Get the most common tags from entries."""
        from django.db.models import Count
        
        tag_counts = entries.values('tags__name').annotate(tag_count=Count('tags__name')).order_by('-tag_count')
        return tag_counts[0]['tags__name'] if tag_counts else NO_DATA_AVAILABLE

def get_current_streak(entries):
    """Get the current streak of journaling entries."""
    if not entries.exists():
        return 0

    streak = 0
    current_date = now().date()
    sorted_entries = entries.order_by('-timestamp')

    for entry in sorted_entries:
        if entry.timestamp.date() != current_date:
            break

        streak += 1
        current_date -= timedelta(days=1)

    return streak



def get_peak_journaling_time(entries: QuerySet) -> int | None:
    """Get the peak journaling time."""
    if not entries.exists():
        return None

    peak_hour = entries.annotate(hour=ExtractHour('timestamp')).values('hour').annotate(count=Count('id')).order_by('-count').first()
    return peak_hour['hour'] if peak_hour else None


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
def get_sentiment(text: str):
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
    # Extracting polarity and subjectivity
    # Compound score is a normalized score between -1 and 1
    polarity = sentiment_scores['compound']
    subjectivity = (sentiment_scores['pos'] + sentiment_scores['neg'] + sentiment_scores['neu']) / 3  # Approximate subjectivity
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment, polarity, subjectivity

# Example usage
sentiment, polarity, subjectivity = None, None, None
try:
    text = "I love this new feature! It's amazing."
    sentiment, polarity, subjectivity = get_sentiment(text)
    print(f"Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}")
except Exception as e:
    print(f"Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}")
    print(f"Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}")

def get_average_sentiment(entries: QuerySet):
    """Calculate the average sentiment of queryset entries."""
    if not entries.exists():
        return {'avg_polarity': None, 'avg_subjectivity': None}
    return {
        'avg_polarity': entries.aggregate(Avg('polarity'))['polarity__avg'],
        'avg_subjectivity': entries.aggregate(Avg('subjectivity'))['subjectivity__avg']
    }


def get_most_common_emotions(entries):
    """Get the most common emotions from entries."""
    if not entries.exists():
        return NO_DATA_AVAILABLE

    emotion_counts = entries.values('sentiment').annotate(emotion_count=Count('sentiment')).order_by('-emotion_count')
    return emotion_counts[0] if emotion_counts else NO_DATA_AVAILABLE




def get_average_word_count(entries):
    if not entries.exists():
        return 0

    total_words = entries.annotate(word_count=Length(F('content')) - Length(F('content')) + Value(1)).aggregate(total=Sum('word_count'))['total']
    return total_words // entries.count() if total_words else 0
