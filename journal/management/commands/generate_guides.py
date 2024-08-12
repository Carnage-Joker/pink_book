import os
import openai
import random
from django.core.management.base import BaseCommand
from journal.models import Guide

openai.api_key = os.getenv("OPENAI_API_KEY")

# Predefined list of topics relevant to sissies
TOPICS = [
    "How to dress elegantly as a sissy",
    "Building confidence in public as a sissy",
    "Understanding sissy fashion trends",
    "Tips for maintaining a sissy persona",
    "Sissy self-care and beauty routines",
    "Navigating relationships as a sissy",
    "Exploring your feminine side",
    "Sissy etiquette in social situations",
    "Balancing sissy life with everyday responsibilities",
    "Creating a sissy-inspired home environment"
]


class Command(BaseCommand):
    help = 'Generates diverse and consistently good sissy guides using OpenAI and posts them in the admin.'

    def handle(self, *args, **kwargs):
        # Randomly select a topic from the list
        topic = random.choice(TOPICS)

        # Generate content using OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a knowledgeable and friendly sissy. Write a humanized, detailed, and high-quality guide about '{topic}' in a sissy-like tone."},
                {"role": "user", "content": f"Generate a guide on the topic: {topic}."},
            ]
        )

        content = response['choices'][0]['message']['content']

        # Implement a basic quality check
        if len(content) < 100:
            self.stdout.write(self.style.ERROR(
                'Generated content is too short. Try again.'))
            return

        # Save the generated content to the database
        guide = Guide.objects.create(
            title=topic,
            content=content
        )
        guide.save()

        self.stdout.write(self.style.SUCCESS(f"Sissy guide on '{
                          topic}' generated and saved successfully."))
