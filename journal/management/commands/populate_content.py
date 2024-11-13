import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import random
from django.core.management.base import BaseCommand
from journal.models import BlogPost, Resource, Guide, Question, Answer, Thread, Post, Comment
from django.contrib.auth import get_user_model
from django.utils import timezone

# Set up OpenAI API key

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with resources, guides, FAQs, Q&A, and threads with posts and comments'

    sissy_topics = [
        "Latest sissy fashion trends and styles",
        "Step-by-step makeup tutorials for sissies",
        "Skincare tips and routines for glowing skin",
        "Creative and fun outfit ideas for sissies",
        "Tips on accessorizing to enhance your sissy look",
        "Hairstyles and hair care tips for sissies",
        "Nail art designs and tutorials",
        "Self-care routines and practices for sissies",
        "Tips and exercises to boost confidence",
        "Stories of inspirational sissy role models",
        "Embracing and loving your body as a sissy",
        "Feminine hygiene tips and products",
        "Personal growth and self-improvement for sissies",
        "DIY fashion and beauty projects",
        "Planning and attending sissy-themed events"
    ]

    def generate_content(self, prompt):
        try:
            response = client.chat.completions.create(model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates content for a sissy lifestyle website called Pink Book."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1024,
            n=1,
            temperature=0.7)
            content = response.choices[0].message.content.strip()
            return content
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error generating content: {e}"))
            return None

    def handle(self, *args, **kwargs):
        self.populate_resources()
        self.populate_guides()
        self.populate_faqs()
        self.populate_qna()
        self.populate_threads()
        self.populate_blog_comments()
        self.stdout.write(self.style.SUCCESS(
            "Database successfully populated with content!"))

    def get_random_topic(self):
        return random.choice(self.sissy_topics)

    def populate_resources(self):
        for i in range(10):
            title = f"Resource Title {i+1}"
            topic = self.get_random_topic()
            description = self.generate_content(
                f"Generate a description for a sissy resource titled '{title}' on the topic '{topic}'")
            if description:
                link = f"https://example.com/resource-{i+1}"
                resource = Resource.objects.create(
                    title=title,
                    description=description,
                    link=link
                )
                resource.save()
            else:
                self.stdout.write(self.style.WARNING(f"Skipping resource '{
                                  title}' due to failed content generation."))

    def populate_guides(self):
        for i in range(10):
            title = f"Guide Title {i+1}"
            topic = self.get_random_topic()
            content = self.generate_content(f"Write a comprehensive guide for sissies titled '{
                                            title}' on the topic '{topic}'")
            if content:
                guide = Guide.objects.create(
                    title=title,
                    content=content,
                    author="Sissy Sparkles"
                )
                guide.save()
            else:
                self.stdout.write(self.style.WARNING(f"Skipping guide '{
                                  title}' due to failed content generation."))

    def populate_faqs(self):
        for i in range(10):
            topic = self.get_random_topic()
            question_content = self.generate_content(
                f"Generate a frequently asked question for sissies on the topic '{topic}'")
            answer_content = self.generate_content(
                f"Provide a detailed answer to the question: '{question_content}'")
            if question_content and answer_content:
                question = Question.objects.create(
                    user=User.objects.first(),  # Assuming there's at least one user
                    question=question_content
                )
                question.save()
                answer = Answer.objects.create(
                    question=question,
                    answer=answer_content,
                    professional=User.objects.first()
                )
                answer.save()
            else:
                self.stdout.write(self.style.WARNING(
                    f"Skipping FAQ '{question_content}' due to failed content generation."))

    def populate_qna(self):
        for i in range(10):
            topic = self.get_random_topic()
            question_content = self.generate_content(
                f"Generate a question for sissies on the topic '{topic}'")
            answer_content = self.generate_content(
                f"Provide a detailed answer to the question: '{question_content}'")
            if question_content and answer_content:
                question = Question.objects.create(
                    user=User.objects.first(),  # Assuming there's at least one user
                    question=question_content
                )
                question.save()
                answer = Answer.objects.create(
                    question=question,
                    answer=answer_content,
                    professional=User.objects.first()
                )
                answer.save()
            else:
                self.stdout.write(self.style.WARNING(
                    f"Skipping Q&A '{question_content}' due to failed content generation."))

    def populate_threads(self):
        for i in range(5):
            title = f"Thread Title {i+1}"
            topic = self.get_random_topic()
            content = self.generate_content(f"Generate a starting post for a thread titled '{
                                            title}' on the topic '{topic}'")
            if content:
                thread = Thread.objects.create(
                    title=title,
                    content=content
                )
                thread.save()

                for j in range(5):
                    post_content = self.generate_content(f"Generate a reply post for the thread '{
                                                         title}' on the topic '{topic}' with user interactions")
                    if post_content:
                        post = Post.objects.create(
                            title=f"Re: {title}",
                            content=post_content,
                            author=User.objects.first(),  # Assuming there's at least one user
                            thread=thread
                        )
                        post.save()
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipping post in thread '{
                                          title}' due to failed content generation."))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping thread '{
                                  title}' due to failed content generation."))

    def populate_blog_comments(self):
        for post in BlogPost.objects.all():
            for i in range(3):
                comment_content = self.generate_content(
                    f"Write a relevant comment for a blog post titled '{post.title}'")
                if comment_content:
                    comment = Comment.objects.create(
                        user=User.objects.first(),  # Assuming there's at least one user
                        content_object=post,
                        content=comment_content
                    )
                    comment.save()
                else:
                    self.stdout.write(self.style.WARNING(f"Skipping comment for blog post '{
                                      post.title}' due to failed content generation."))
