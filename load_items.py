import os
from django.core.management.base import BaseCommand
from dressup.models import Item, Shop


class Command(BaseCommand):
    help = 'Load dressup items into the database'

    def handle(self, *args, **kwargs):
        # Define the base path where images are stored
        base_path = 'C:/Users/Sir_f/source/repos/NewPinkBook/dressup/static/avatars' # Update with the correct path

        # Map categories to their subfolders
        categories = {
            'hair': 'hair',
            'top': 'tops',
            'bottom': 'skirts',
            'shoes': 'shoes',
            'accessory': 'accessories',
            # Add other categories as necessary
        }

        for category, folder in categories.items():
            folder_path = os.path.join(base_path, folder)
            if not os.path.exists(folder_path):
                self.stdout.write(self.style.WARNING(
                    f"Folder {folder_path} does not exist. Skipping."))
                continue

            for filename in os.listdir(folder_path):
                # Ensure valid image formats
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0].replace(
                        '_', ' ').title()  # Create a user-friendly name
                    # Relative path from static root
                    image_path = f"{folder}/{filename}"

                    # Check if the item already exists
                    if not Item.objects.filter(name=name, category=category).exists():
                        # Create the item
                        item = Item.objects.create(
                            category=category,
                            name=name,
                            image_path=image_path,
                            # Default price (adjust as needed)
                            price_points=100,
                            price_dollars=0,   # Free for now
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f"Added {item.name} to {category}"))
                    else:
                        self.stdout.write(f"Item {name} already exists.")
