from django.contrib.auth import get_user_model
import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# Ensure this is your actual user model import
from journal.models import CustomUser

from .utils import get_default_user

 # virtual_try_on/models.py


class Pose(models.Model):
    POSE_CHOICES = [
        ('standing', 'Standing'),
        ('sitting_lady', 'Sitting ladylike'),
        ('sitting_legspread', 'Sitting slutspread'),
        ('lying_facedown', 'Lying ass up'),
        ('kneeling', 'On knees'),
        ('dancing', 'Dancing')
    ]
    name = models.CharField(max_length=100, choices=POSE_CHOICES)
    image = models.ImageField(upload_to='poses/')

    def __str__(self):
        return self.name


class Environment(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='environments/')

    def __str__(self):
        return self.name


class PremiumOutfit(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='premium_outfits/')
    description = models.TextField(blank=True, default='none')
    price = models.DecimalField(max_digits=4, decimal_places=2,
                                default=Decimal('0.00'))

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('outfit_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
        verbose_name = "Premium Outfit"
        verbose_name_plural = "Premium Outfits"


# Other model definitions...
BODY_TYPE_CHOICES = [
    ('hourglass', 'Hourglass'),
    ('thick', 'Thick'),
    ('slim', 'Slim'),
    ('straight', 'Straight')
]
SKIN_TONE_CHOICES = [
    ('light', 'Light'),
    ('brown', 'Brown'),
    ('dark', 'Dark'),
]
HAIR_STYLE_CHOICES = [
    ('long_straight', 'Long Straight'),
    ('long_curly', 'Long Curly'),
    ('short_straight', 'Short Straight'),
    ('short_curly', 'Short Curly'),
    ('bob', 'Bobcut'),
]
HAIR_COLOR_CHOICES = [
    ('black', 'Black'),
    ('brown', 'Brunette'),
    ('blonde', 'Blonde'),
    ('red', 'Red'),
    ('pink', 'Pink'),
]


# virtual_try_on/models.py


class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('skirt', 'Skirt'),
        ('dress', 'Dress'),
        ('shoes', 'Shoes')
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image_url = models.CharField(max_length=255)
    is_premium = models.BooleanField(default=False)


class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('skirt', 'Skirt'),
        ('dress', 'Dress'),
        ('shoes', 'Shoes')
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image_url = models.CharField(max_length=255)
    is_premium = models.BooleanField(default=False)


class Avatar(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    body_type = models.CharField(max_length=255)
    skin_tone = models.CharField(max_length=255)
    hair_type = models.CharField(max_length=255)
    hair_color = models.CharField(max_length=255)
    top = models.ForeignKey(ClothingItem, related_name='avatar_top',
                            on_delete=models.SET_NULL, null=True, blank=True)
    skirt = models.ForeignKey(ClothingItem, related_name='avatar_skirt',
                              on_delete=models.SET_NULL, null=True, blank=True)
    dress = models.ForeignKey(ClothingItem, related_name='avatar_dress',
                              on_delete=models.SET_NULL, null=True, blank=True)
    shoes = models.ForeignKey(ClothingItem, related_name='avatar_shoes',
                              on_delete=models.SET_NULL, null=True, blank=True)

    def get_body_image_path(self):
        return f"/static/virtual_try_on/avatars/body/{self.skin_tone}/{self.body_type}.png"

    def get_hair_image_path(self):
        return f"/static/virtual_try_on/avatars/hair/{self.hair_type}/{self.hair_color}.png"

    def get_top_image_path(self):
        return self.top.image_url if self.top else "/static/virtual_try_on/garmets/tops/1.png"

    def get_skirt_image_path(self):
        return self.skirt.image_url if self.skirt else "/static/virtual_try_on/garmets/skirts/1.png"

    def get_dress_image_path(self):
        return self.dress.image_url if self.dress else "/static/virtual_try_on/garmets/dresses/1.png"

    def get_shoes_image_path(self):
        return self.shoes.image_url if self.shoes else "/static/virtual_try_on/garmets/shoes/1.png"

def initialize_user_avatar(user):
    avatar, created = Avatar.objects.get_or_create(user=user)
    if created:
        # Assign default clothing items
        default_items = ClothingItem.objects.filter(is_premium=False)
        avatar.top = default_items.filter(category='top').first()
        avatar.skirt = default_items.filter(category='skirt').first()
        avatar.dress = default_items.filter(category='dress').first()
        avatar.shoes = default_items.filter(category='shoes').first()
        avatar.save()


class Feature(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    outfit = models.ForeignKey(
        PremiumOutfit, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Favorite outfit {self.outfit.name} for {self.user.sissy_name}"
    