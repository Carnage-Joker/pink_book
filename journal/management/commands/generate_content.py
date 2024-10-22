import openai
import random
from django.core.management.base import BaseCommand
from journal.models import BlogPost, Comment, Faq, Guide, JournalEntry, Quote, Report, Tag, Thread, Post, CustomUser
from django.utils import timezone
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

# Predefined unique blog post topics
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

SSY_TOPICS = [
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

# Function to generate text using OpenAI's chat API


def generate_text(prompt, max_tokens=400, temperature=0.85):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates engaging and unique content for a sissy-themed lifestyle website. Be flirty, fun, and embrace a bimbo-submissive tone. Make sure the content is creative, interesting, and unique to each prompt."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response['choices'][0]['message']['content'].strip()

# Generate blog post comments that are specific to the post content


def generate_comments(post, num_comments=2):
    for _ in range(num_comments):
        comment_prompt = f"Write a playful, flirty, sissy-themed comment on the blog post titled '{
            post.title}', referencing the content. Make sure the comment feels personal and related to the content."
        comment_text = generate_text(comment_prompt, max_tokens=150)
        Comment.objects.create(
            user=random.choice(CustomUser.objects.all()
                               ),  # Choose a random user
            content_object=post,
            content=comment_text,
            timestamp=timezone.now(),
        )

# Generate tags


def generate_tags(num_tags=15):
    for _ in range(num_tags):
        tag_name = generate_text(
            "Generate a unique and catchy tag for a sissy lifestyle blog", max_tokens=5)
        Tag.objects.create(name=tag_name)


class Command(BaseCommand):
    help = "Generate diverse blog posts, comments, FAQs, guides, and other content with a sissy theme"

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()

        # Shuffle topics to ensure we generate unique posts
        random.shuffle(TOPICS)
        random.shuffle(SSY_TOPICS)

        # Generate Blog Posts and Comments
        # Generate 10 unique blog posts
        for i, topic in enumerate(TOPICS[:10]):
            post_prompt = f"Write a unique and engaging blog post about the topic: '{
                topic}'. Make sure the tone is playful, flirty, and encourages sissies to embrace their bimbo-submissive lifestyle."
            title = topic
            content = generate_text(post_prompt, max_tokens=600)
            blog_post = BlogPost.objects.create(
                title=title,
                content=content,
                author="Sissy Sparkles",
                timestamp=timezone.now(),
                published=True,
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created blog post: {title}"))
            # Generate comments that relate to the post content
            generate_comments(blog_post)

        # Generate FAQs
        for _ in range(10):
            question_prompt = "Write a frequently asked question from a sissy who is curious about the lifestyle and submissive roles."
            answer_prompt = "Answer this question in a flirty, bimbo-ish way that encourages sissies to embrace their role and subtly encourages them to stay in the lifestyle."
            question = generate_text(question_prompt, max_tokens=15)
            answer = generate_text(answer_prompt, max_tokens=150)
            Faq.objects.create(
                question=question,
                answer=answer
            )
            self.stdout.write(self.style.SUCCESS(f"Created FAQ: {question}"))

        # Generate Guides
        # Generate 5 unique guides
        for i, ssy_topic in enumerate(SSY_TOPICS[:5]):
            guide_prompt = f"Write a detailed, engaging guide for sissies about the topic: '{
                ssy_topic}'. It should be flirty, fun, and encourage sissies to fully embrace their lifestyle."
            guide_title = ssy_topic
            guide_content = generate_text(guide_prompt, max_tokens=1000)
            Guide.objects.create(
                title=guide_title,
                content=guide_content,
                author="Sissy Guide",
                created_at=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created guide: {guide_title}"))

        # Generate Journal Entries for each user
        for user in users:
            for _ in range(2):  # Two journal entries per user
                journal_prompt = f"Write a personal journal entry from the perspective of a sissy exploring the lifestyle. Make it reflective and include feelings of submission, bimbo-ness, and excitement."
                entry_title = generate_text(
                    f"Generate a journal entry title for a sissy user", max_tokens=10)
                entry_content = generate_text(journal_prompt, max_tokens=500)
                JournalEntry.objects.create(
                    user=user,
                    title=entry_title,
                    content=entry_content,
                    timestamp=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Created journal entry for user {user.sissy_name}"))

        # Generate Quotes
        for _ in range(10):
            quote_prompt = "Generate a motivational quote that encourages sissies to embrace their submissive, bimbo-ish lifestyle."
            quote = generate_text(quote_prompt, max_tokens=30)
            Quote.objects.create(
                content=quote,
                author="Sissy Inspiration",
                timestamp=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f"Created quote: {quote}"))

        # Generate Reports
        for _ in range(3):
            report_prompt = "Generate a reason for reporting inappropriate content on a sissy-themed website."
            report_reason = generate_text(report_prompt, max_tokens=20)
            Report.objects.create(
                # Random content to report
                content_object=random.choice(BlogPost.objects.all()),
                reason=report_reason,
                reported_by=random.choice(users),
                timestamp=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created report: {report_reason}"))

        # Generate Tags
        generate_tags(15)

        # Generate Threads and Posts
        for _ in range(7):
            thread_title = generate_text(
                "Generate a thread title related to sissification", max_tokens=10)
            thread_content = generate_text(
                "Write an engaging introductory post to start a thread about sissy life", max_tokens=400)
            thread = Thread.objects.create(
                title=thread_title, content=thread_content)
            self.stdout.write(self.style.SUCCESS(
                f"Created thread: {thread_title}"))

            for _ in range(7):
                post_content = generate_text(f"Write a bimbo-ish post in the thread '{
                                             thread_title}' that encourages discussion", max_tokens=250)
                Post.objects.create(
                    title="Discussion Post",
                    content=post_content,
                    author=random.choice(users),
                    thread=thread,
                    timestamp=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Created post in thread: {thread_title}"))
