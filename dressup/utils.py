# utils.py
from .models import FavoriteOutfit, ClothingItem
from django.contrib.auth import get_user_model


def get_default_user():
    ##function to get the default user
    return get_user_model().objects.get_or_create(username='defaultuser')[0]


def add_clothing_to_favorites(user, clothing_item):
    favorite_outfit, created = FavoriteOutfit.objects.get_or_create(
        user=user, outfit_name='Favorite Outfit')
    favorite_outfit.clothing_items.add(clothing_item)
    favorite_outfit.save()


def get_premium_items():
    return ClothingItem.objects.filter(is_premium=True)
