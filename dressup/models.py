from django.db import models
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from journal.models import CustomUser  # Ensure correct import path

User = get_user_model()

# =====================
# Item Model
# =====================


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
        ('jewellery', 'Jewellery'),
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

    def save(self, *args, **kwargs):
        if self.image_path and not self.image_path.startswith('dressup/'):
            raise ValueError("Image path must start with 'dressup/'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================
# Shop Model
# =====================
class Shop(models.Model):
    SHOP_TYPE_CHOICES = [
        ('salon', 'Salon'),
        ('thrift_shop', 'Thrift Shop'),
        ('high_end', 'High-End Department'),
        ('designer', 'Designer'),
        ('jewellery', 'Jewellery'),
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
    items = models.ManyToManyField(Item, related_name='shop_items')
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image_path = models.CharField(max_length=200, blank=True, null=True)

    def get_image_url(self):
        return static(self.image_path or f'dressup/shops/default.svg')

    def __str__(self):
        return self.name


# =====================
# Avatar Model
# =====================
class Avatar(models.Model):
    BODY_CHOICES = [('00', 'Straight'), ('01', 'Petite'),
                    ('02', 'Curvy'), ('03', 'Hourglass')]
    SKIN_CHOICES = [('00', 'Light'), ('01', 'Tan'), ('02', 'Dark')]
    HAIR_CHOICES = [('00', 'Short'), ('01', 'Wavy Bangs'),
                    ('02', 'Long Straight')]
    HAIR_COLOR_CHOICES = [('black', 'Black'), ('brunette', 'Brunette'),
                          ('blonde', 'Blonde'), ('red', 'Red'), ('pink', 'Pink')]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='sissy_avatar')
    name = models.CharField(max_length=100, default="Sissy Avatar")
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=20, choices=HAIR_CHOICES, default='00')
    hair_color = models.CharField(
        max_length=20, choices=HAIR_COLOR_CHOICES, default='black')
    story_started = models.BooleanField(default=False)
    equipped_items = models.ManyToManyField(
        Item, related_name='equipped_on_avatars', blank=True)

    def get_image_urls(self, layer_keys=None):
        if layer_keys is None:
            layer_keys = ['body', 'hair', 'skirt',
                          'top', 'shoes', 'accessories']
        urls = {
            'body': static(f'dressup/avatars/body/{self.body}/{self.skin}.png'),
            'hair': static(f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png'),
        }
        for key in layer_keys:
            if key not in urls:
                urls[key] = static(f'dressup/avatars/{key}/00.png')
        for item in self.equipped_items.all():
            if item.category in layer_keys:
                urls[item.category] = static(item.image_path)
        return urls

    def equip_item(self, item):
        self.equipped_items.filter(category=item.category).delete()
        self.equipped_items.add(item)
        self.save()

    def unequip_item(self, item):
        self.equipped_items.remove(item)
        self.save()

    @property
    def equipped_display_names(self):
        return {item.category: item.name for item in self.equipped_items.all()}

    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"


# =====================
# Purchased Item Model
# =====================
class PurchasedItem(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='purchased_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.sissy_name} purchased {self.item.name}"


# =====================
# PhotoShoot Model
# =====================
class PhotoShoot(models.Model):
    PHOTOGRAPHER_CHOICES = [
        ('booth', 'Photo Booth'),
        ('creepy', 'Creepy Photographer'),
        ('hot', 'Hot Photographer'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photographer_type = models.CharField(
        max_length=20, choices=PHOTOGRAPHER_CHOICES)
    backdrop = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photoshoots/')
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.sissy_name}'s photoshoot with {self.photographer_type} photographer"


# =====================
# Optional: Leaderboard Model
# =====================
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.sissy_name}: {self.points} points"
