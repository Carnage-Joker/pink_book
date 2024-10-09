from time import timezone

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Avatar Model


class Avatar(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='avatar'
    )
    body = models.ImageField(upload_to='avatars/body/', max_length=100)
    hair = models.ImageField(upload_to='avatars/hair/', max_length=100)
    eyes = models.ImageField(upload_to='avatars/eyes/', max_length=100)
    top = models.ImageField(upload_to='avatars/top/',
                            max_length=100, blank=True, null=True)
    bottom = models.ImageField(
        upload_to='avatars/bottom/', max_length=100, blank=True, null=True)
    shoes = models.ImageField(
        upload_to='avatars/shoes/', max_length=100, blank=True, null=True)
    accessories = models.ImageField(
        upload_to='avatars/accessories/', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Avatar"

# ClothingItem Model


class ClothingItem(models.Model):
    TYPE_CHOICES = [
        ('TOP', 'Top'),
        ('BOTTOM', 'Bottom'),
        ('DRESS', 'Dress'),
        ('SHOES', 'Shoes'),
        ('ACCESSORY', 'Accessory'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='clothing_items/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Premium' if self.is_premium else 'Free'})"

# FavoriteOutfit Model


class FavoriteOutfit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_outfits'
    )
    outfit_name = models.CharField(max_length=100)
    clothing_items = models.ManyToManyField(ClothingItem)

    def __str__(self):
        return f"{self.user.username}'s Favorite Outfit: {self.outfit_name}"

# PhotoshootLocation Model


class PhotoshootLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photoshoot_locations/')
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Premium' if self.is_premium else 'Free'})"

# Item Model for Purchasing System


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('TOP', 'Top'),
        ('BOTTOM', 'Bottom'),
        ('SHOES', 'Shoes'),
        ('ACCESSORY', 'Accessories'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Premium' if self.is_premium else 'Free'})"

# PurchasedItem Model to Track Purchases


class PurchasedItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchased_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} purchased {self.item.name}"
