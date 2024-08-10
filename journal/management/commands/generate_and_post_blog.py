import os
import openai
import time
import random
from django.core.management.base import BaseCommand
from journal.models import BlogPost

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class Command(BaseCommand):
    help = 'Generate and post blog entries for the Pink Book'

    themes = [
        "Self-Acceptance: Embracing your sissy identity and loving yourself.",
        "Fashion Tips: Latest sissy fashion trends, outfits, and styling tips.",
        "Makeup and Beauty: Makeup tutorials, beauty routines, and skincare tips.",
        "Personal Growth: Overcoming challenges and growing as a sissy.",
        "Relationships: Navigating relationships as a sissy.",
        "Coming Out: Stories and advice on coming out as a sissy.",
        "Community Support: Finding and building a supportive sissy community.",
        "Role Models: Inspirational sissy role models and their stories.",
        "Sissy Lifestyle: Daily life and routines of a sissy.",
        "Mental Health: Managing mental health and well-being as a sissy.",
        "Fitness and Health: Staying fit and healthy while embracing your femininity.",
        "Hobbies and Interests: Exploring hobbies and interests that align with sissy values.",
        "Sissy Challenges: Participating in and overcoming sissy challenges.",
        "Personal Stories: Sharing personal experiences and journeys.",
        "Books and Media: Reviews and recommendations of sissy-related books, movies, and shows.",
        "Events and Meetups: Attending sissy events and meetups.",
        "DIY Projects: DIY fashion, accessories, and home decor for sissies.",
        "Sissy Goals: Setting and achieving personal goals.",
        "Support Systems: Building and maintaining a strong support system.",
        "Sissy Etiquette: Manners and etiquette for sissies in different social situations.",
        "Shopping Tips: Best places to shop for sissy clothes and accessories.",
        "Sissy History: Historical figures and movements related to the sissy community.",
        "Creative Expression: Exploring creative outlets like art, writing, and music.",
        "Confidence Building: Boosting confidence and self-esteem as a sissy.",
        "Work and Career: Balancing a professional life with your sissy identity.",
        "Exploring Desires: Understanding and exploring your sissy desires and fantasies.",
        "Mindfulness and Meditation: Practices to stay centered and mindful.",
        "Sissy Inspirations: Inspirational quotes and stories to motivate and uplift.",
        "Adventures and Travel: Traveling and exploring new places as a sissy.",
        "Sissy Activism: Advocating for sissy rights and visibility."
    ]

    def generate_blog_post(self):
        theme = random.choice(self.themes)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that writes blog posts for a sissy lifestyle website called Pink Book. The posts should be positive, inspiring, and relevant to the sissy community. Do not label the title or content of the post."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a blog post for a sissy lifestyle website called Pink Book. The theme of the post is '{theme}'. The post should be at least 500 words long and focus on the theme. The tone should be friendly, supportive, and engaging. The post should include tips, advice, or personal anecdotes that resonate with sissies. The post should encourage sissies to embrace their femininity, explore their desires, and connect with others in the community. The post should be written in a casual, conversational style that is easy to read and understand. The post should avoid explicit content, offensive language, but should playfully explore innuendo within a sissy context and themes. The post should be original, creative, and engaging to keep readers interested and inspired."
                    }
                ],
                max_tokens=4800,
                temperature=0.7,
            )
            content = response.choices[0].message['content'].strip()
            # Extract the title and content from the response
            title, content = self.extract_title_and_content(content)
            return title, content
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error generating blog post: {e}"))
            return None, None

    def extract_title_and_content(self, text):
        # Simple method to split the title from the content
        lines = text.split('\n')
        title = lines[0].strip()
        content = '\n'.join(lines[1:]).strip()
        return title, content

    def check_content(self, content):
        if len(content) < 100 or "spam" in content.lower():
            return False
        if content.isnumeric():
            return False
        return True

    def post_to_django_admin(self, title, content):
        try:
            new_post = BlogPost.objects.create(
                title=title,
                content=content,
                author="Sissy Admin"
            )
            new_post.save()
            self.stdout.write(self.style.SUCCESS(
                "Blog post successfully created!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error creating blog post: {e}"))

    def handle(self, *args, **kwargs):
        while True:
            self.stdout.write("Generating blog post...")
            title, content = self.generate_blog_post()

            if title and content and self.check_content(content):
                self.stdout.write(
                    "Content looks good. Posting to Django admin...")
                self.post_to_django_admin(title, content)
            else:
                self.stdout.write(self.style.WARNING(
                    "Generated content did not pass the quality check."))

            # Wait for 1 hour before generating the next post (3600 seconds)
            time.sleep(1000)
