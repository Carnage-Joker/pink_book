import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import random
from django.utils import timezone
from journal.models import BlogPost, Comment, Faq, Quote

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate blog posts using AI'

    def handle(self, *args, **options):
        generate_blog_posts()
        create_faq()
        generate_quotes()
        self.stdout.write(self.style.SUCCESS(
            'Blog posts, FAQs, and quotes generated successfully.'))

# Your OpenAI API key


# A list of blog topics you want to generate content for
BLOG_TOPICS = [
    "Top 10 Must-Have Accessories to Elevate Your Feminine Style",
    "Sissification Hypnosis: How It Works and Its Benefits",
    "How to Create a Feminine Home Environment",
    "Top 10 Feminine Hobbies to Try",
    "The Role of Diet and Exercise in Sissy Transformation",
    "How to Walk Gracefully in Heels",
    "Essential Body Language Tips for Sissies",
    "Choosing the Right Fragrance to Enhance Your Femininity",
    "How to Develop Your Sissy Persona",
    "How to Find Sissy-Friendly Clothing Stores",
]

# Comments to add to the generated posts
COMMENT_TEMPLATES = [
    "OMG! This is such good advice, thank you so much for sharing, lovely! 💖",
    "I absolutely adore this! I’m going to try these tips out this weekend.",
    "This blog post is everything. You totally captured my sissy journey!",
    "I never thought of that, such an amazing tip! 🌸",
    "Thank you so much for this insight! It’s exactly what I needed today."
]

# FAQ questions and answers
FAQ_QUESTIONS = [
    ("What is the best way to start feminizing?",
     "Start with small steps, like adopting feminine habits or makeup."),
    ("How do I develop a more feminine voice?",
     "Voice training is key! Practice speaking softly and with a higher pitch."),
    ("Where can I find sissy-friendly stores?",
     "Look for online communities or stores that cater to sissies, such as FemStyle."),
    ("How do I walk in heels?",
     "Start by practicing on flat surfaces, then move to different terrains."),
    ("What is a sissy chastity device?",
     "A sissy chastity device is a tool used for controlling and enhancing femininity."),
]

# Prompts to feed into the GPT-4 model, with specific instruction for high-quality content
PROMPT_TEMPLATE = """
Write a high-quality, unique blog post on the topic "{topic}". Use a modern, fun, and engaging tone with playful, catty, and sissified energy. Ensure the post is fresh, welcoming, and full of feminine charm. Include relevant tips and advice for sissies, such as makeup suggestions, wardrobe ideas, or sissy-related life tips. Avoid outdated language and repetition. Be literal, visually descriptive, and make sure the content is always lively, confident, and inclusive, with a hint of sass!
"""

# Function to generate blog content using GPT-4 Chat model


def generate_blog_content(topic):
    prompt = PROMPT_TEMPLATE.format(topic=topic)
    try:
        # Using the ChatCompletion method of GPT-4
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a highly creative and engaging blog writer specializing in sissy lifestyle content. Your style is modern, fun, and catty while being welcoming and inclusive."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200,
        temperature=0.85)
        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Error generating content for {topic}: {str(e)}")
        return None

# Function to create a blog post and save it to the database


def create_blog_post(topic, content):
    post = BlogPost.objects.create(
        title=topic,
        content=content,
        published=True,  # Set as published if you want it live immediately
        timestamp=timezone.now(),
    )
    print(f"Blog post '{post.title}' created.")
    return post

# Function to create comments for a blog post


def create_comments(post):
    for _ in range(random.randint(1, 3)):  # Add 1-3 comments randomly
        content = random.choice(COMMENT_TEMPLATES)
        comment = Comment.objects.create(
            post=post,
            comment=content,
            timestamp=timezone.now(),
        )
        print(f"Comment added to post '{post.title}'.")

# Function to create FAQs and save to the database


def create_faq():
    for question, answer in FAQ_QUESTIONS:
        faq = Faq.objects.create(
            question=question,
            answer=answer,
        )
        print(f"FAQ created: '{faq.question}'.")

# Function to generate blog posts with comments


def generate_blog_posts():
    for topic in BLOG_TOPICS:
        content = generate_blog_content(topic)
        if content:
            post = create_blog_post(topic, content)
            create_comments(post)  # Add comments to each post

# Function to generate random quotes


def generate_quotes():
    quotes = [
        "Embrace your femininity, darling. It's your superpower.",
        "Never underestimate the power of heels and a good outfit.",
        "You're not just a sissy; you're a queen in the making.",
        "Femininity is a journey, not a destination. Enjoy the process."
    ]
    for quote_text in quotes:
        quote = Quote.objects.create(
            content=quote_text, timestamp=timezone.now())
        print(f"Quote created: {quote.content}")


# Call functions to generate and post content
generate_blog_posts()
create_faq()
generate_quotes()
