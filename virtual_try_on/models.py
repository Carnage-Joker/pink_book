# virtual_try_on/models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import datetime
from django.db import models
from decimal import Decimal
# Ensure this is your actual user model import
from journal.models import CustomUser


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
        return self.get_name_display()


class Environment(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='environments/')

    def __str__(self):
        return self.name


class PremiumOutfit(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='premium_outfits/')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'))

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


def get_default_user():
    user = get_user_model()
    try:
        # Return the primary key of the first user in the database
        return user.objects.first().pk
    except (AttributeError, ObjectDoesNotExist):
        # Handle the case where no user exists
        return user.objects.create().pk


class Avatar(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=get_default_user)
    body_type = models.CharField(
        choices=BODY_TYPE_CHOICES, max_length=20, default='hourglass')
    skin_tone = models.CharField(
        max_length=20, choices=SKIN_TONE_CHOICES, default='light')
    hair_style = models.CharField(
        choices=HAIR_STYLE_CHOICES, max_length=50, default='long_straight')
    hair_color = models.CharField(
        choices=HAIR_COLOR_CHOICES, max_length=20, default='black')
    outfit = models.CharField(max_length=100)
    accessories = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"


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
