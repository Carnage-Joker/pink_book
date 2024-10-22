import random
from django.core.management.base import BaseCommand
from journal.models import Resource, ResourceCategory

# Categories for resources
RESOURCE_CATEGORIES = [
    "Sissy Fashion & Clothing",
    "Makeup & Beauty Guides",
    "Sissy Etiquette & Behavior",
    "Roleplaying & Feminization",
    "Sissy Sexuality & Fetish",
    "Community & Forums",
    "Personal Growth & Confidence",
    "Shopping & Accessories"
]

# Resource templates for each category
RESOURCE_DATA = {
    "Sissy Fashion & Clothing": [
        {"title": "Frilly Delights", "description": "Shop specializing in sissy clothing, from maid outfits to frilly dresses.", "link": "https://frillydelights.com"},
        {"title": "The Sissy Boutique", "description": "Custom-made sissy attire with a range of elegant and playful designs.", "link": "https://sissyboutique.com"},
    ],
    "Makeup & Beauty Guides": [
        {"title": "Makeup for Sissies", "description": "Step-by-step makeup tutorials for sissies to create a soft, feminine look.", "link": "https://makeup4sissies.com"},
        {"title": "Feminine Beauty Secrets", "description": "Beauty tips and routines to help sissies achieve flawless skin.", "link": "https://femininebeautysecrets.com"},
    ],
    "Sissy Etiquette & Behavior": [
        {"title": "The Sissy’s Guide to Proper Etiquette", "description": "Learn how to behave and present yourself with the grace of a sissy.", "link": "https://sissyetiquetteguide.com"},
    ],
    "Roleplaying & Feminization": [
        {"title": "Embrace Your Feminine Side", "description": "Articles on embracing your sissy role, with a focus on feminization techniques.", "link": "https://embraceyourfeminine.com"},
    ],
    "Sissy Sexuality & Fetish": [
        {"title": "Sissy Chastity 101", "description": "A guide to sissy chastity devices and sexual play.", "link": "https://sissychastity101.com"},
    ],
    "Community & Forums": [
        {"title": "Sissy Chat Forum", "description": "A welcoming community for sissies to discuss their journey and share experiences.", "link": "https://sissychatforum.com"},
    ],
    "Personal Growth & Confidence": [
        {"title": "Building Confidence as a Sissy", "description": "Resources on becoming confident in public as a sissy.", "link": "https://sissyconfidence.com"},
    ],
    "Shopping & Accessories": [
        {"title": "Sissy Heels", "description": "A shop dedicated to high heels perfect for the sissy lifestyle.", "link": "https://sissyheels.com"},
        {"title": "Sissy Accessories", "description": "Shop for bows, ribbons, and feminine jewelry tailored for sissies.", "link": "https://sissyaccessories.com"},
    ],
}

class Command(BaseCommand):
    help = 'Populate the resources section for sissies with high-quality, relevant tools, articles, and shops.'

    def handle(self, *args, **kwargs):
        # Iterate through categories and populate resources
        for category, resources in RESOURCE_DATA.items():
            for resource in resources:
                # Check if the resource already exists to avoid duplicates
                if not Resource.objects.filter(title=resource['title']).exists():
                    Resource.objects.create(
                        category=ResourceCategory,
                        title=resource['title'],
                        description=resource['description'],
                        link=resource['link'],
                    )
                    print(f"Resource '{resource['title']}' added to {category} section.")
        print("Resources successfully populated!")
