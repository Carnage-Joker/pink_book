from django.db import models
from django.templatetags.static import static
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    CATEGORY_CHOICES = (
        ('body', 'Body'),
        ('hair', 'Hair'),
        ('top', 'Tops'),
        ('skirt', 'Skirts'),
        ('top', 'Tops'),
        ('skirt', 'Skirts'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessories'),
        ('accessory', 'Accessories'),
        ('makeup', 'Makeup'),
        ('wig', 'Wigs'),
        ('wig', 'Wigs'),
        ('jewellery', 'Jewellery'),
        ('lingerie', 'Lingerie'),
        ('background', 'Backgrounds'),
        ('background', 'Backgrounds'),
    )

    name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_path = models.CharField(max_length=200, blank=True, null=True)
    price_points = models.IntegerField(default=0, blank=True, null=True)
    price_dollars = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.image_path and not self.image_path.startswith('dressup/'):
            raise ValueError(f"Invalid image path '{self.image_path}': must start with 'dressup/'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Shop(models.Model):
    SHOP_TYPE_CHOICES = (
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
    )
    SHOP_LEVEL_CHOICES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('cute', 'Cute'),
        ('hawt', 'Hawt'),
        ('sexy', 'Sexy'),
    )
    SHOP_LEVEL_CHOICES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('cute', 'Cute'),
        ('hawt', 'Hawt'),
        ('sexy', 'Sexy'),
    )

    name = models.CharField(max_length=100)
    shop_id = models.CharField(max_length=100, blank=True, null=True)
    shop_id = models.CharField(max_length=100, blank=True, null=True)
    shop_type = models.CharField(max_length=50, choices=SHOP_TYPE_CHOICES)
    shop_level = models.CharField(
        max_length=50, choices=SHOP_LEVEL_CHOICES, default='basic')
    items = models.ManyToManyField(Item, related_name='shop_items')
    shop_level = models.CharField(
        max_length=50, choices=SHOP_LEVEL_CHOICES, default='basic')
    items = models.ManyToManyField(Item, related_name='shop_items')
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image_path = models.CharField(max_length=200, blank=True, null=True)

    def get_image_url(self):
        default_image = 'dressup/shops/default.svg'
        try:
            return static(f'dressup/shops/{self.shop_level}/{self.shop_type}.jpg')
        except Exception:
            return static(default_image)

    def __str__(self):
        return self.name


User = get_user_model()


class Avatar(models.Model):
    BODY_CHOICES = [
        ('00', 'straight_body'),
        ('01', 'petite_body'),
        ('02', 'curvy_body'),
        ('03', 'hourglass_body'),
    ]

    SKIN_CHOICES = [
        ('00', 'light'),
        ('01', 'tan'),
        ('02', 'dark'),
    ]

    HAIR_CHOICES = [
        ('00', 'short_hair'),
        ('01', 'short_wavy_bangs'),
        ('02', 'long_straight_hair'),
    ]

    HAIR_COLOR_CHOICES = [
        ('00', 'Black'),
        ('01', 'Brunette'),
        ('02', 'Blonde'),
        ('03', 'Red'),
        ('04', 'Pink'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='sissy_avatar'
    )
    name = models.CharField(max_length=100, default="Sissy Avatar")

    # Avatar core attributes
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=2, choices=HAIR_CHOICES, default='00')
    hair_color = models.CharField(
        max_length=20, choices=HAIR_COLOR_CHOICES, default='00')
    story_started = models.BooleanField(default=False)

    # Equipped items
    equipped_items = models.ManyToManyField(
        'Item',
        related_name='equipped_on_avatars',
        blank=True,
        help_text="Items currently equipped on the avatar."
    )

    def get_image_urls(self):
        """
        Returns a dictionary of image URLs for each avatar component.
        Uses equipped items where available, falling back to default images.
        """
        layers = ['body', 'hair', 'skirt', 'top', 'shoes', 'accessories']
        urls = {
            'body': static(f'dressup/avatars/body/{self.body}/{self.skin}.png'),
            'hair': static(f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png'),
        }

        # Default images for unequipped items
        for layer in layers:
            if layer not in urls:
                urls[layer] = static(f'dressup/avatars/{layer}/00.png')

        # Override with equipped items
        for item in self.equipped_items.all():
            if item.category in layers:
                urls[item.category] = static(item.image_path)

        return urls

    def equip_item(self, item):
        """
        Equips an item, ensuring only one item per category is equipped.
        """
        if not item.category:
            raise ValueError("Item must have a category to be equipped.")

        # Unequip any existing item in the same category
        self.equipped_items.filter(category=item.category).delete()

        # Equip the new item
        self.equipped_items.add(item)
        self.save()

    def unequip_item(self, item):
        """
        Unequips an item from the avatar.
        """
        self.equipped_items.remove(item)
        self.save()

    @property
    def equipped_display_names(self):
        """
        Returns a dictionary of display names for equipped items.
        """
        return {item.category: item.name for item in self.equipped_items.all()}

    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"


class PurchasedItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchased_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True, null=True)
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')

    def equip(self):
        if not self.is_equipped:
            self.is_equipped = True
            self.save()
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')

    def equip(self):
        if not self.is_equipped:
            self.is_equipped = True
            self.save()

    def __str__(self):
        return f"{self.user.sissy_name} purchased {self.item.name}"


class PhotoShoot(models.Model):
    PHOTOGRAPHER_CHOICES = (
        ('photo_booth', 'Photo Booth'),
        ('creepy', 'Creepy Photographer'),
        ('hot', 'Hot Photographer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photographer_type = models.CharField(
        max_length=20, choices=PHOTOGRAPHER_CHOICES)
    # Assuming backdrops are items
    backdrop = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photoshoots/')
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.sissy_name}'s photoshoot with {self.photographer_type} photographer"


# Optionally, you can create a model to cache leaderboard data
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
