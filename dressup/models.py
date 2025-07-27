from __future__ import annotations
from django.db import models
from django.templatetags.static import static
from django.contrib.auth import get_user_model
import os
from github import Github
from github.GithubIntegration import GithubIntegration

from django.conf import settings



class Item(models.Model):
    CATEGORY_CHOICES = [
        ('body', 'Body'),
        ('hair', 'Hair'),
        ('top', 'Top'),
        ('skirt', 'Skirt'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('makeup', 'Makeup'),
        ('wig', 'Wig'),
        ('lingerie', 'Lingerie'),
        ('background', 'Background'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_path = models.CharField(max_length=200, blank=True, null=True)
    price_points = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    price_dollars = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    shop = models.ManyToManyField('Shop', related_name='items', blank=True)

    def _validate_image_path(self):
        if self.image_path and not self.image_path.startswith('dressup/'):
            raise ValueError("Image path must start with 'dressup/'.")

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: list[str] | None = None,
        *args,
        **kwargs
    ) -> None:
        self._validate_image_path()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            *args,
            **kwargs
        )

    def __str__(self):
        return self.name


class Shop(models.Model):
    SHOP_TYPE_CHOICES = [
        ('salon', 'Salon'),
        ('thrift_shop', 'Thrift Shop'),
        ('high_end', 'High-End Department'),
        ('designer', 'Designer'),
        ('lingerie', 'Lingerie'),
        ('shoes', 'Shoes'),
        ('designer_shoes', 'Designer Shoes'),
        ('wig_shop', 'Wig Shop'),
        ('gym', 'Gym'),
        ('bank', 'Bank'),
        ('photography_studio', 'Photography Studio'),
    ]

    SHOP_LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('cute', 'Cute'),
        ('hawt', 'Hawt'),
        ('sexy', 'Sexy'),
    ]

    name = models.CharField(max_length=100)
    shop_id = models.CharField(max_length=100, blank=True, null=True)
    shop_type = models.CharField(max_length=50, choices=SHOP_TYPE_CHOICES)
    shop_level = models.CharField(
        max_length=50, choices=SHOP_LEVEL_CHOICES, default='basic')
    item = models.ManyToManyField(Item, related_name='shop_item')
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image_path = models.CharField(max_length=200, blank=True, null=True)

    def get_image_url(self):
        return static(self.image_path or 'dressup/shops/default.svg')

    def __str__(self):
        return self.name


class Avatar(models.Model):
    BODY_CHOICES = [('00', 'Straight'), ('01', 'Petite'),
                    ('02', 'Curvy'), ('03', 'Hourglass')]
    SKIN_CHOICES = [('00', 'Light'), ('01', 'Tan'), ('02', 'Dark')]
    HAIR_CHOICES = [('00', 'Short'), ('01', 'Wavy Bangs'),
                    ('02', 'Long Straight')]
    HAIR_COLOR_CHOICES = [('black', 'Black'), ('brunette', 'Brunette'),
                          ('blonde', 'Blonde'), ('red', 'Red'), ('pink', 'Pink')]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sissy_avatar',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, default="Avatar")
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=2, choices=HAIR_CHOICES, default='00')
    hair_color = models.CharField(
        max_length=20, choices=HAIR_COLOR_CHOICES, default='black')
    story_started = models.BooleanField(default=False)
    outfit_name = models.CharField(max_length=100, blank=True, null=True)
    equipped_item = models.ManyToManyField(
        Item, related_name='item', blank=True)

    def get_image_urls(self, layer_keys: list[str] | None = None) -> dict[str, str]:
        if layer_keys is None:
            layer_keys = ['body', 'hair', 'top',
                          'skirt', 'shoes', 'accessories']
        urls = {
            'body': static(f'dressup/avatars/body/{self.body}/{self.skin}.png'),
            'hair': static(f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png')
        }
        for key in layer_keys:
            if key not in urls:
                urls[key] = static(f'dressup/avatars/{key}/00.png')
        for item in self.equipped_item.all():
            if item.category in layer_keys and item.image_path:
                urls[item.category] = static(item.image_path)
        return urls

    def equip_item(self, item):
        if not isinstance(item, Item):
            raise ValueError("Expected an Item instance.")
        self.equipped_item.remove(*self.equipped_item.filter(category=item.category))
        self.equipped_item.add(item)
        self.save()

    def unequip_item(self, item):
        self.equipped_item.remove(item)
        self.save()

    @property
    def equipped_display_names(self):
        return {item.category: item.name for item in self.equipped_item.all()}

    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"


class SavedOutfit(models.Model):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, related_name='saved_outfit')
    name = models.CharField(max_length=100)
    top = models.CharField(max_length=20)
    skirt = models.CharField(max_length=20)
    shoes = models.CharField(max_length=20)
    accessory = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.avatar.user.sissy_name}"


class PurchasedItem(models.Model):
    avatar = models.ForeignKey(
        Avatar, on_delete=models.CASCADE, related_name='purchased_item')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('avatar', 'item')

    def __str__(self):
        return f"{self.avatar.user.sissy_name} purchased {self.item.name}"


class PhotoShoot(models.Model):
    PHOTOGRAPHER_CHOICES = [
        ('booth', 'Photo Booth'),
        ('creepy', 'Creepy Photographer'),
        ('hot', 'Hot Photographer'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photo_shoots',
        null=True,
        blank=True,
    )
    photographer_type = models.CharField(
        max_length=20, choices=PHOTOGRAPHER_CHOICES)
    backdrop = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photoshoots/')
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.sissy_name}'s photoshoot with {self.photographer_type} photographer"

class LeaderboardEntry(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries',
        null=True,
        blank=True,
    )
    points = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.sissy_name}: {self.points} points"


# GitHub App Configuration (leave unchanged)
GH_APP_ID_ENV = os.getenv("GH_APP_ID")
GH_INSTALL_ID_ENV = os.getenv("GH_INSTALL_ID")
GH_WEBHOOK_SECRET = os.getenv("GH_WEBHOOK_SECRET")
GH_APP_KEY_PATH = os.getenv("GH_APP_KEY_PATH")
LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
REPO_FULL = os.getenv("REPO_FULL", "carnage-joker/pink_book")

GH_APP_ID = int(GH_APP_ID_ENV) if GH_APP_ID_ENV is not None else None
GH_INSTALL_ID = int(GH_INSTALL_ID_ENV) if GH_INSTALL_ID_ENV is not None else None


def get_github() -> Github:
    try:
        if GH_APP_ID is None or GH_INSTALL_ID is None:
            raise RuntimeError("GH_APP_ID and GH_INSTALL_ID must be set")
        if GH_APP_KEY_PATH is None:
            raise RuntimeError("GH_APP_KEY_PATH is not set")
        with open(GH_APP_KEY_PATH, "r") as f:
            key = f.read()
        integration = GithubIntegration(GH_APP_ID, key)
        token = integration.get_access_token(GH_INSTALL_ID).token
        return Github(token)
    except FileNotFoundError:
        raise RuntimeError(f"Key file not found: {GH_APP_KEY_PATH}")
    except Exception as e:
        raise RuntimeError(f"GitHub auth failed: {e}")
