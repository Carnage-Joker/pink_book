# models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static

User = get_user_model()


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('body', 'Body'),
        ('hair', 'Hair'),
        ('top', 'Top'),
        ('skirt', 'Skirt'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
        ('makeup', 'Makeup'),
        ('wig', 'Wig'),
        ('jewellery', 'Jewellery'),
        ('lingerie', 'Lingerie'),
        ('background', 'Background'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_path = models.CharField(max_length=200, blank=True, null=True)
    price_points = models.IntegerField(default=0, blank=True, null=True)
    price_dollars = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)

    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def save(self, *args: tuple, **kwargs: dict) -> None:
        """
        Mandatory safety check to ensure images are stored under 'dressup/'.
        """
        if self.image_path and not self.image_path.strip().startswith('dressup/'):
            raise ValueError(
                f"Invalid image path '{self.image_path}': must start with 'dressup/' "
                "and be a valid relative path."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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
        """
        Returns the static path for this shop’s image if it exists,
        otherwise a default path.
        """
        default_image = 'dressup/shops/default.svg'
        if self.shop_level and self.shop_type:
            return static(f'dressup/shops/{self.shop_level}/{self.shop_type}.jpg')
        return static(default_image)

    def __str__(self):
        return self.name


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
        User,
        on_delete=models.CASCADE,
        related_name='sissy_avatar'
    )
    name = models.CharField(max_length=100, default="Sissy Avatar")

    # Avatar core attributes
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=2, choices=HAIR_CHOICES, default='00')
    hair_color = models.CharField(
        max_length=2, choices=HAIR_COLOR_CHOICES, default='00')
    story_started = models.BooleanField(default=False)

    # Additional direct code fields for top, skirt, shoes, and accessory
    top = models.CharField(max_length=2, default='00')
    skirt = models.CharField(max_length=2, default='00')
    shoes = models.CharField(max_length=2, default='00')
    accessory = models.CharField(max_length=2, default='00')

    # Equipped items (M2M for items purchased/owned)
    equipped_items = models.ManyToManyField(
        Item,
        related_name='equipped_on_avatars',
        blank=True,
        help_text="Items currently equipped on the avatar."
    )

    def get_image_urls(self):
        """
        Returns a dictionary mapping layer names to static image paths.
        This uses the avatar’s own body/hair/top/skirt/shoes/accessory settings
        and overrides them with any equipped items in matching categories.
        """
        layers = ['body', 'hair', 'skirt', 'top', 'shoes', 'accessories']
        urls = {
            'body': static(f'dressup/avatars/body/{self.body}/{self.skin}.png'),
            'hair': static(f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png'),
            'skirt': static(f'dressup/avatars/skirt/{self.skirt}.png'),
            'top': static(f'dressup/avatars/top/{self.top}.png'),
            'shoes': static(f'dressup/avatars/shoes/{self.shoes}.png'),
            'accessories': static(f'dressup/avatars/accessory/{self.accessory}.png'),
        }

        # Override with any M2M equipped items
        for item in self.equipped_items.all():
            if item.category in layers:
                urls[item.category] = static(item.image_path)

        return urls

    def equip_item(self, item: Item):
        """
        Equips an item, ensuring only one item per category is equipped in M2M.
        """
        if not item.category:
            raise ValueError("Item must have a category to be equipped.")

        # Remove currently equipped item(s) of the same category
        same_cat_items = self.equipped_items.filter(category=item.category)
        for eq_item in same_cat_items:
            self.equipped_items.remove(eq_item)

        # Now equip the new item
        self.equipped_items.add(item)
        self.save()

    def unequip_item(self, item: Item):
        """
        Unequips an item from the avatar (removes it from M2M).
        """
        self.equipped_items.remove(item)
        self.save()

    @property
    def equipped_display_names(self):
        """
        Returns a dictionary of display names for equipped items,
        keyed by category, e.g. {'top': 'Tank Top', 'shoes': 'Sneakers'}.
        """
        return {item.category: item.name for item in self.equipped_items.all()}

    def __str__(self):
        # If your custom user model has a 'sissy_name' field:
        return f"{self.user.sissy_name}'s Avatar"


class PurchasedItem(models.Model):
    """
    Tracks which user purchased which Item, and whether it’s used or equipped.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchased_items'
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True, null=True)
    is_equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')

    def equip(self):
        if not self.is_equipped:
            self.is_equipped = True
            self.save()

    def __str__(self):
        # Also using 'sissy_name' if your CustomUser has it:
        return f"{self.user.sissy_name} purchased {self.item.name}"


class PhotoShoot(models.Model):
    PHOTOGRAPHER_CHOICES = [
        ('photo_booth', 'Photo Booth'),
        ('creepy', 'Creepy Photographer'),
        ('hot', 'Hot Photographer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photographer_type = models.CharField(
        max_length=20, choices=PHOTOGRAPHER_CHOICES)
    backdrop = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photoshoots/')
    used = models.BooleanField(default=False)

    def __str__(self):
        # Or any other user field you'd like to display
        return f"{self.user.sissy_name}'s photoshoot with {self.photographer_type}"
