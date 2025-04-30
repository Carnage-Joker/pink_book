import logging
from collections import Counter
from datetime import timedelta

from django.db.models import Avg, Count, F, IntegerField, Sum, Value
from django.db.models.functions import ExtractHour, Length
from django.db.models import Avg, Count, F, IntegerField, Sum, Value
from django.db.models.functions import ExtractHour, Length
from django.db.models.query import QuerySet
from django.utils.timezone import now
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
logger = logging.getLogger(__name__)

NO_DATA_AVAILABLE = 'No data available'


from typing import Dict, List, Union, Optional


def get_dashboard_insights(entries: QuerySet['JournalEntry'], habits: QuerySet, todos: QuerySet) -> Dict[str, Union[int, str, None, List[str]]]:
    """Collect all insights for the user's dashboard."""
    if not entries.exists():
        return get_default_insights()

    avg_sentiment = calculate_avg_sentiment(entries)

    return {
        'habit_consistency': get_habit_consistency(habits),
        'weekly_reflection_count': get_weekly_reflection_count(entries),
        'chores_completed': get_chores_completed(todos),
        'avg_sentiment': avg_sentiment,
        'most_common_tags': get_most_common_tags(entries),
        'current_streak': get_current_streak(entries),
        'peak_journaling_time': get_peak_journaling_time(entries),
        'habit_sentiment': analyze_habit_sentiment_correlation(entries, habits)
    }

def get_default_insights() -> Dict[str, Union[int, str, None, List[str]]]:
    """Return default insights when no entries are available."""
    return {
        'habit_consistency': 0,
        'weekly_reflection_count': 0,
        'chores_completed': 0,
        'avg_sentiment': NO_DATA_AVAILABLE,
        'most_common_tags': NO_DATA_AVAILABLE,
        'current_streak': 0,
        'peak_journaling_time': NO_DATA_AVAILABLE,
        'habit_sentiment': NO_DATA_AVAILABLE
    }
def calculate_avg_sentiment(entries: QuerySet) -> str:
    """Calculate the average sentiment from entries."""
    avg_sentiment_score = entries.aggregate(Avg('polarity'))['polarity__avg']
    if avg_sentiment_score is None:
        return NO_DATA_AVAILABLE

    if avg_sentiment_score > 0:
        return 'positive'
    elif avg_sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'


def get_most_common_tags(entries: QuerySet) -> str:
    """Get the most common tags from journal entries."""
    if not entries.exists():
        return NO_DATA_AVAILABLE

    # Convert QuerySet to a list if it has been sliced
    if hasattr(entries, '_result_cache') and entries._result_cache is not None:
        tag_counts = list(
            entries.values('tags__name')
            .annotate(tag_count=Count('tags__name'))
        )
        # Use Python sorting
        tag_counts.sort(key=lambda x: x['tag_count'], reverse=True)
    else:
        tag_counts = (
            entries.values('tags__name')
            .annotate(tag_count=Count('tags__name'))
            .order_by('-tag_count')  # Safe only if slicing has not occurred
        )

    return tag_counts[0]['tags__name'] if tag_counts else NO_DATA_AVAILABLE

def get_habit_consistency(habits):
    """Calculate habit consistency as a percentage."""
    if not habits.exists():
        return 0

    total_habits = len(habits)
    completed_habits = sum(1 for habit in habits if habit.is_completed())

    return round((completed_habits / total_habits) * 100) if total_habits else 0


def get_weekly_reflection_count(entries: QuerySet) -> int:
    """Calculate the number of reflections made in the past week."""
    one_week_ago = now() - timedelta(days=7)
    return entries.filter(timestamp__gte=one_week_ago).count()



def get_chores_completed(todos: QuerySet) -> int:
    """Calculate the number of completed chores."""
    return todos.filter(category="chore_tasks", completed=True).count()


def get_current_streak(entries: QuerySet) -> int:
    if not entries.exists():
        return 0

    # ✅ Apply order_by first
    entries = entries.order_by('-timestamp')

    streak = 0
    current_date = now().date()
    sorted_entries = entries.order_by('-timestamp')

    for entry in sorted_entries:
        if entry.timestamp.date() != current_date:
            break

        streak += 1
        current_date -= timedelta(days=1)


    return streak


def get_peak_journaling_time(entries: QuerySet) -> Optional[int]:
    """Get the peak journaling time."""
    if not entries.exists():
        return None

    peak_hour = (
        entries.annotate(hour=ExtractHour('timestamp'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    return peak_hour['hour'] if peak_hour else None


def extract_keywords(entries, num_keywords=10):
    """Extract the most common keywords from journal entries."""
    if not entries.exists():
        return []

    text = ' '.join(entry.content for entry in entries)

    if len(text.split()) < num_keywords:
        return []

    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.isalpha(
    ) and word not in stopwords.words('english')]
    most_common = Counter(filtered_tokens).most_common(num_keywords)
    return most_common  # List of tuples (keyword, count)


def get_sentiment(text: str) -> tuple[str, float, float]:
    """Analyze the sentiment of a given text using VADER."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)

    polarity = sentiment_scores['compound']
    subjectivity = (sentiment_scores['pos'] + sentiment_scores['neg'] +
                    sentiment_scores['neu']) / 3  # Approximate subjectivity
    sentiment = 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'

    return sentiment, polarity, subjectivity


def get_average_sentiment(entries: QuerySet):
    """Calculate the average sentiment of journal entries."""
    if not entries.exists():
        return {'avg_polarity': None, 'avg_subjectivity': None}

    return {
        'avg_polarity': entries.aggregate(Avg('polarity'))['polarity__avg'],
        'avg_subjectivity': entries.aggregate(Avg('subjectivity'))['subjectivity__avg']
    }

def get_average_word_count(entries: QuerySet):
    """Calculate the average word count of journal entries."""
    if not entries.exists():
        return None

    return entries.aggregate(avg_word_count=Avg(Length('content', output_field=IntegerField())))['avg_word_count']

def analyze_habit_sentiment_correlation(entries, habits):
    """Determine whether habits are improving or worsening the user's mood."""
    if not entries.exists() or not habits.exists():
        return NO_DATA_AVAILABLE

    habit_names = [habit.name for habit in habits]
    habit_related_entries = entries.filter(content__icontains=habit_names[0])
    for habit_name in habit_names[1:]:
        habit_related_entries = habit_related_entries | entries.filter(content__icontains=habit_name)

    sentiment_data = {habit_name: [] for habit_name in habit_names}

    for entry in habit_related_entries:
        for habit_name in habit_names:
            if habit_name in entry.content:
                sentiment_data[habit_name].append(get_sentiment(entry.content)[1])

    positive_habits = 0
    neutral_habits = 0
    negative_habits = 0

    for habit_name, sentiments in sentiment_data.items():
        if sentiments:
            avg_polarity = sum(sentiments) / len(sentiments)
            if avg_polarity > 0.5:
                positive_habits += 1
            elif avg_polarity < -0.3:
                negative_habits += 1
            else:
                neutral_habits += 1

    if positive_habits > negative_habits:
        return "Your habits are making a **positive impact** on your mood! Keep it up! 😊"
    elif negative_habits > positive_habits:
        return "Some habits seem to be **affecting your mood negatively**. Consider adjusting them. 💭"
    else:
        return "Your habits have a **neutral** impact on your emotions. Maybe try writing about them more? ✍️"
