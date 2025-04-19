import os
from django.core.management.base import BaseCommand
from django.conf import settings
from dressup.models import Item


class Command(BaseCommand):
    help = "Imports items (tops, skirts, shoes, accessories, etc.) from static folders into the Item model."

    def handle(self, *args, **options):
        """
        Example script that looks in /static/items/<category> and adds them to the DB.
        Adjust category lists, paths, or price defaults as needed.
        """
        # Define the categories and the corresponding subfolders
        category_map = {
            'top': 'top',
            'skirt': 'skirt',
            'shoes': 'shoes',
            'accessory': 'accessory'
            # Add more if you have them: 'hair': 'hair', etc.
        }

        # Base path to your static/items folder:
        items_base_path = os.path.join(
            settings.BASE_DIR, 'dressup', 'static', 'items')

        # For each category, scan files in the folder
        for category, folder_name in category_map.items():
            folder_path = os.path.join(items_base_path, folder_name)
            if not os.path.isdir(folder_path):
                self.stdout.write(self.style.WARNING(
                    f"Folder not found: {folder_path}. Skipping {category}."
                ))
                continue

            # List all PNG files
            files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            files.sort()  # optional: sort numerically

            for filename in files:
                # We'll store in DB as 'dressup/items/<folder_name>/<filename>'
                relative_path = f"dressup/items/{folder_name}/{filename}"

                # Remove file extension if you want the item name to be just '00' etc.
                name_without_ext = os.path.splitext(filename)[0]

                # Check if an item with this image_path already exists
                if Item.objects.filter(image_path=relative_path).exists():
                    self.stdout.write(self.style.NOTICE(
                        f"Item already exists: {relative_path} (skipping)."
                    ))
                    continue

                # Create a new Item
                new_item = Item.objects.create(
                    # e.g. 'Top 01'
                    name=f"{folder_name.capitalize()} {name_without_ext}",
                    category=category,
                    image_path=relative_path,
                    price_points=0,
                    price_dollars=0,
                    premium_only=False,
                    is_locked=False,
                    description=f"A cute {folder_name} for sissies!"
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Created Item: {new_item.name} (image_path={relative_path})"
                ))

        self.stdout.write(self.style.SUCCESS("Item import complete!"))
