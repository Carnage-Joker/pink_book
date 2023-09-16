import os
import requests
import random
from textblob import TextBlob
from django.db.models import Avg
from collections import Counter
import re
from django.db.models import QuerySet
import openai
import logging




API_KEY = os.environ.get('OPEN_AI_KEY', 'default_value')
openai.api_key = os.getenv("OPEN_AI_KEY")

GENERIC_PROMPTS =[
    "How did your day go?",
    "What's on your mind right now?",
    "Describe an event from today that stood out to you.",
    "How are you feeling at this very moment?",
    "What's one thing you learned today?",
    "Write about a challenge you faced recently.",
    "Describe something beautiful you witnessed today.",
    "What's a goal you're working towards right now?",
    "Is there something you're looking forward to?",
    "How has your week been so far?"
]
SORRY_SISSY_MESSAGES = [
                    'Oh dear, this is embarrassing','we will be back up in no time babe', 'oh princess, no insights today...','what a shame, no insights today...']

THEMES = [
      'Emotional Experiences', 'The Process of Feminization', 'Assigned Sissy Tasks', 
    'Encountered Challenges', 'Personal Fantasies', 'Fashion & Style', 'Skill Building', 
    'Relationship Dynamics', 'Confidence & Self-Esteem', 'Community & Support', 
    'Daily Rituals', 'Milestones & Achievements', 'Self-Care & Wellness', 
    'Role Models & Inspirations', 'Future Goals & Aspirations', 'Sexual Experiences', 'stereotypes','femininity',
    'hypnos'
]
def get_dynamic_prompt(recent_entries):
    theme = random.choice(THEMES)
    recent_keywords = get_frequent_keywords(recent_entries)
    ai_extension = get_chatgpt_prompt(theme, theme, recent_keywords)
    return ai_extension

def get_overall_insight(entries, sissy_name):
    combined_text = ' '.join([entry.content for entry in entries])
    if len(combined_text) > 0:  # Don't bother if there's nothing to analyze, sweetie!
        insight = get_entry_insights(combined_text, sissy_name)
        return insight
    else:
        return "Oh, darling, there are no entries to analyze yet!"

def get_collective_insight(user, JournalEntry):
    all_entries = JournalEntry.objects.filter(user=user)
    concatenated_entries = " ".join([entry.content for entry in all_entries])
    collective_insight = get_entry_insights(concatenated_entries, user.sissy_name)
    # Update the dashboard here, possibly by saving the insight to the user model
    return collective_insight


def get_chatgpt_prompt(prompt_text, theme, recent_keywords=None):

    data = {
        "prompt": f"Provide a journaling prompt that caters specifically to a member of the sissy community, inspiring them to write with reflection and insight. The theme is {theme}.",
        "max_tokens": 25
         
    }
    if recent_keywords:
        data['prompt'] += f" Consider incorporating these recent themes or keywords: {', '.join(recent_keywords)}"
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages="messages"
        )
        print("API Response:", response)  # Print the API response for debugging

        if isinstance(response, dict):
            ai_output = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if not ai_output:
                ai_output = random.choice(GENERIC_PROMPTS)
        else:
            print(f"Unexpected response type: {type(response)}")
            ai_output = random.choice(GENERIC_PROMPTS)

        return ai_output
    except Exception as e:
        print(f"Error occurred: {e}")
        return random.choice(GENERIC_PROMPTS)

logger = logging.getLogger(__name__)

def get_entry_insights(entries, sissy_name):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Here's the secure way, darling!
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=[
                {"role": "system", "content": "You are a helpful expert in sissification, feminization, and mental health. Keep your responses short and concise. Your tone should be conversational but a little vague"},
                {"role": "user", "content": f"Provide insight from the following diary entry.{entries} Offer short and snappy but helpful advice, with no explaination "},
            ]
        )
        print("API Response:", response)  # Just for debugging, sweetie!
        
        if isinstance(response, dict):
            ai_insight = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if not ai_insight:
                ai_insight = "Oh, something went wrong, darling!"  # Or any default message
        else:
            print(f"Unexpected response type: {type(response)}")
            ai_insight = "Sorry, darling, something went wrong!"  # Or any default message

        return ai_insight
    except Exception as e:
        print(f"Oops, an error occurred: {e}")
        return "Sorry, darling, something went wrong!"  # Or any default message




def get_average_sentiment(entries: QuerySet):
    if entries.exists():  # Check if there are any entries, sweetie!
        avg_polarity = entries.aggregate(Avg('polarity'))['polarity__avg']
        avg_subjectivity = entries.aggregate(Avg('subjectivity'))['subjectivity__avg']
        return avg_polarity, avg_subjectivity
    else:
        return None, None  # Return None if no entries exist, darling.


def get_frequent_keywords(entries: QuerySet):
    if entries.exists():  # Again, check for entries!
        all_text = " ".join(entry.content for entry in entries)
        words = re.findall(r'\w+', all_text.lower())
        return Counter(words).most_common(5)
    else:
        return []  # Empty list if no entries, love.

   
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.polarity
    subjectivity = blob.subjectivity
    return polarity, subjectivity






