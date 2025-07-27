from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint, sample
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Seed the database with sissy-themed test data for all models.'

    def handle(self, *args, **options):
        fake = Faker()

        # Import models
        from journal.models import (
            CustomUser, Habit, ToDo, Guide, Notification,
            Question, Answer, BlogPost, Resource, ResourceCategory,
            ResourceComment, Contact, Moderator, Task, JournalEntry,
            TaskCompletion, Report, Quote, Thread, UserProfile,
            Comment, Post, UserFeedback, Tag, UserTheme,
            Streak, Billing, Message, ActivityLog, Faq
        )
        from dressup.models import (
            Item, Shop, Avatar, SavedOutfit, PurchasedItem,
            PhotoShoot, LeaderboardEntry
        )

        # Predefined sissy-themed content
        sissy_blog_posts = [
            {
                'title': 'Embracing Your Inner Sissy: A Beginner\'s Guide',
                'content': 'Discover the essentials of sissy dressing, makeup tips, and confidence-building exercises to fully embrace your feminine side.'
            },
            {
                'title': 'Top 10 Sissy-Approved Lingerie Picks',
                'content': 'From lacy panties to satin babydolls, explore the most flattering lingerie for every sissy body type.'
            },
            {
                'title': 'Sissy Skirt Styles: How to Flaunt Your Legs',
                'content': 'A deep dive into cute skirt silhouettes, styling tricks, and must-have accessories for the perfect sissy look.'
            },
        ]

        sissy_guides = [
            {'title': 'Makeup Masterclass for Sissies',
                'content': 'Step-by-step tutorial on achieving a flawless pink-palette look with glitter and bold lashes.'},
            {'title': 'Sissy Walk 101',
                'content': 'How to glide gracefully in heels: posture drills, heel height recommendations, and safety tips.'},
            {'title': 'Building a Sissy Capsule Wardrobe',
                'content': 'Essential pieces every sissy needs: camisoles, tutus, pastel accessories, and more.'},
        ]

        sissy_faqs = [
            {'question': 'What is a sissy?',
                'answer': 'A sissy is someone who embraces feminine attire and mannerisms as part of their identity or kink.'},
            {'question': 'How do I choose the right lingerie?',
                'answer': 'Measure your waist and hips, choose soft fabrics, and start with pastel colors if you\'re new.'},
            {'question': 'Is sissy dressing safe?',
                'answer': 'Yes, with the right fit and materials. Always practice in a private space first.'},
        ]

        sissy_threads = [
            {'title': 'Favorite sissy-friendly boutiques',
                'content': 'Share your go-to shops for cute skirts and accessories!'},
            {'title': 'Heels that won\'t kill your feet',
                'content': 'Discuss shoe brands that balance style and comfort.'},
            {'title': 'Lip gloss recs for sissies',
                'content': 'Best long-lasting pink and glitter glosses—share your swatches!'},
        ]

        sissy_quotes = [
            {'content': '\"Be a lady? No, be a sissy!\"', 'author': 'Sparkles'},
            {'content': '\"High heels, higher confidence.\"', 'author': 'Lady Lace'},
            {'content': '\"Every day is a sissy parade.\"', 'author': 'Miss Pink'},
        ]

        # Create users (idempotent)
        users = []
        for _ in range(5):
            u, _ = CustomUser.objects.get_or_create(
                email=fake.unique.email(),
                defaults={'sissy_name': fake.unique.user_name()}
            )
            u.set_password('password123')
            u.save()
            users.append(u)
        admin, _ = CustomUser.objects.get_or_create(
            email='admin@example.com',
            defaults={'sissy_name': 'admin',
                      'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('password123')
        admin.save()
        users.append(admin)

        # Profiles & Themes
        for user in users:
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'privacy_level': 'public',
                          'nsfw_blur': False, 'insight_opt': True}
            )
            UserTheme.objects.get_or_create(
                user=user,
                defaults={'color': 'pastel-pink', 'layout': 'card'}
            )

        # Tags
        tags = []
        for word in ['sissy', 'femme', 'pink', 'lace', 'heels']:
            tags.append(Tag.objects.get_or_create(
                name=word, defaults={'description': f'{word} tag'})[0])

        # Sissy Blog Posts
        for post in sissy_blog_posts:
            BlogPost.objects.get_or_create(
                title=post['title'],
                defaults={
                    'content': post['content'],
                    'author': choice(users).sissy_name,
                    'published': True
                }
            )

        # Sissy Guides
        for guide in sissy_guides:
            Guide.objects.get_or_create(
                title=guide['title'],
                defaults={'content': guide['content'], 'author': 'Admin'}
            )

        # FAQs
        for faq in sissy_faqs:
            Faq.objects.get_or_create(
                question=faq['question'],
                defaults={'answer': faq['answer']}
            )

        # Threads & Posts
        for thread in sissy_threads:
            t, _ = Thread.objects.get_or_create(
                title=thread['title'],
                defaults={'content': thread['content']}
            )
            # add a sample post
            Post.objects.get_or_create(
                title=thread['title'] + ' Post',
                defaults={'content': thread['content'],
                          'author': choice(users), 'thread': t}
            )

        # Quotes
        for q in sissy_quotes:
            Quote.objects.get_or_create(content=q['content'], defaults={
                                        'author': q['author']})

        self.stdout.write(self.style.SUCCESS(
            '✅ Sissy-themed data seeded successfully.'))
