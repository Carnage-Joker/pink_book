from journal.models import BlogPost, Comment
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import os
import openai
import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from journal.models import BlogPost, Comment, Faq, Quote

# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# List of blog topics
BLOG_TOPICS = [
    "How to Dress Elegantly as a Sissy",
    "Building Confidence in Public as a Sissy",
    "Understanding Sissy Fashion Trends",
    "Tips for Maintaining a Sissy Persona",
    "Sissy Self-Care and Beauty Routines",
    "Navigating Relationships as a Sissy",
    "Exploring Your Feminine Side",
    "Sissy Etiquette in Social Situations",
    "Balancing Sissy Life with Everyday Responsibilities",
    "Creating a Sissy-Inspired Home Environment"
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

# Comments to add to the generated posts
COMMENT_TEMPLATES = [
    "OMG! This is such good advice, thank you so much for sharing, lovely! 💖",
    "I absolutely adore this! I’m going to try these tips out this weekend.",
    "This blog post is everything. You totally captured my sissy journey!",
    "I never thought of that, such an amazing tip! 🌸",
    "Thank you so much for this insight! It’s exactly what I needed today."
]

# Prompt template for generating blog content
PROMPT_TEMPLATE = """Write a blog post about "{topic}" for sissies. Include tips, advice, and personal experiences to help sissies embrace their femininity and express themselves confidently. The post should be engaging, informative, supportive, and full of sass and femininity!"""

# Command class for Django management


class Command(BaseCommand):
    help = 'Generate and post blog content, FAQs, and quotes'

    def handle(self, *args, **kwargs):
        generate_blog_posts()
        create_faq()
        generate_quotes()

# Function to generate blog content using OpenAI Chat model


def generate_blog_content(topic):
    prompt = PROMPT_TEMPLATE.format(topic=topic)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a highly creative and engaging blog writer specializing in sissy lifestyle content. Your style is modern, fun, and catty while being welcoming and inclusive."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.85,  # Increased for more creativity
            presence_penalty=0.7,  # Encourage unique content
            frequency_penalty=0.6,  # Reduce repetition
        )
        content = response['choices'][0]['message']['content'].strip()
        return content
    except Exception as e:
        print(f"Error generating content for {topic}: {str(e)}")
        return None

# Function to create a blog post and save to the database


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


CustomUser = get_user_model()


def create_comments(post):
    COMMENT_TEMPLATES = [
        "OMG! This is such good advice, thank you so much for sharing, lovely! 💖",
        "I absolutely adore this! I’m going to try these tips out this weekend.",
        "This blog post is everything. You totally captured my sissy journey!",
        "I never thought of that, such an amazing tip! 🌸",
        "Thank you so much for this insight! It’s exactly what I needed today."
    ]

    # Get the ContentType for the BlogPost model
    content_type = ContentType.objects.get_for_model(BlogPost)

    # Retrieve a superuser to associate with the comment
    if user := CustomUser.objects.filter(is_superuser=True).first():
        for _ in range(random.randint(1, 3)):  # Generate 1-3 random comments
            content = random.choice(COMMENT_TEMPLATES)
            # Create the comment object
            Comment.objects.create(
                content_type=content_type,  # Link to the ContentType for BlogPost
                object_id=post.id,  # Link to the specific BlogPost instance
                user=user,  # Link to the selected CustomUser
                content=content,
                timestamp=timezone.now(),
            )
        print(f"Comments added to post '{post.title}'.")
    else:
        print("No user found to add comments.")

# Function to create FAQs and save to the database


def create_faq():
    for question, answer in FAQ_QUESTIONS:
        Faq.objects.create(
            question=question,
            answer=answer,
        )
    print("FAQs created.")

# Function to generate blog posts with comments


def generate_blog_posts():
    for topic in BLOG_TOPICS:
        content = generate_blog_content(topic)
        if content:
            post = create_blog_post(topic, content)
            create_comments(post)

# Function to generate random quotes


def generate_quotes():
    quotes = [
        "Embrace your femininity, darling. It's your superpower.",
        "Never underestimate the power of heels and a good outfit.",
        "You're not just a sissy; you're a queen in the making.",
        "Femininity is a journey, not a destination. Enjoy the process."
    ]
    for quote_text in quotes:
        Quote.objects.create(content=quote_text, timestamp=timezone.now())
    print("Quotes generated.")

# Main function to run all content creation processes


def main():
    generate_blog_posts()
    create_faq()
    generate_quotes()


# Run the main function when executed as a script
if __name__ == "__main__":
    main()
