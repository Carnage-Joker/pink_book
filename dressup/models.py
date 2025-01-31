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
        ('shoes', 'Shoes'),
        ('accessory', 'Accessories'),
        ('makeup', 'Makeup'),
        ('wig', 'Wigs'),
        ('jewellery', 'Jewellery'),
        ('lingerie', 'Lingerie'),
        ('background', 'Backgrounds'),
    )

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
        default_image = 'dressup/shops/default.svg'
        try:
            return static(f'dressup/shops/{self.shop_level}/{self.shop_type}.svg')
        except Exception:
            return static(default_image)

    def __str__(self):
        return self.name


class Avatar(models.Model):

    BODY_CHOICES = (
        ('01', 'straight_body'),
        ('02', 'curvy_body'),
        ('03', 'hourglass_body'),
        ('04', 'pear_body'),
        ('05', 'apple_body'),
        ('06', 'athletic_body'),
        ('07', 'petite_body'),

        # Add more body types as needed
    )
    SKIN_CHOICES = (
        ('01', 'light'),
        ('02', 'medium'),
        ('03', 'dark'),
        ('04', 'pale'),
        ('05', 'tan'),
    )
    HAIR_CHOICES = (
        ('01', 'short_hair'),
        ('02', 'long_straight_hair'),
        ('03', 'long_curly_hair'),
        ('04', 'long_wavy_hair'),
        ('05', 'bob_cut'),
        ('06', 'pig_tails'),
        # add more feminine hair styles
        ('07', 'bald'),  # for wigs
        ('08', 'short_curly_hair'),
        ('09', 'short_wavy_hair'),
        ('10', 'long_straight_bangs'),
        ('11', 'long_curly_bangs'),
        ('12', 'long_wavy_bangs'),
        ('13', 'bob_cut_bangs'),
        ('14', 'pig_tails_bangs'),
        ('15', 'short_curly_bangs'),
        ('16', 'short_wavy_bangs'),
        # Add more hair styles as needed
    )
    HAIR_COLOR_CHOICES = (
        ('01', 'black'),
        ('02', 'brown'),
        ('03', 'blonde'),
        ('04', 'red'),
        ('05', 'blue'),
        ('06', 'green'),
        ('07', 'purple'),
        ('08', 'pink'),
        ('09', 'rainbow'),
    )

    SHOES_CHOICES = [
        ('00', 'ugly shoes'),  # for sissies who don't deserve nice shoes
        ('01', 'Sneakers'),
        ('02', 'Boots'),
        # Add other girly shoe types
        ('03', 'Heels'),
        ('04', 'Flats'),
        ('05', 'Sandals'),
        ('06', 'Wedges'),
        ('07', 'Mules'),
        ('08', 'Pumps'),
        ('09', 'Platforms'),
        ('10', 'Ankle Boots'),
        ('11', 'Thigh High Boots'),
        ('12', 'Knee High Boots'),
    ]

    ACCESSORIES_CHOICES = [
        ('00', 'None'),
        ('01', 'Hat'),
        ('02', 'Scarf'),
        # Add other feminine accessories
        ('03', 'Gloves'),
        ('04', 'Sunglasses'),
        ('05', 'Handbag'),
        ('06', 'Necklace'),
        ('07', 'Bracelet'),
        ('08', 'Earrings'),
        ('09', 'collar'),
        ('10', 'Belt'),
    ]

    SKIRT_CHOICES = [
        ('00', 'ugly shorts'),  # for sissies who don't deserve skirts
        ('01', 'Mini Skirt'),
        ('02', 'Midi Skirt'),
        # Add other skirt types
        ('03', 'Maxi Skirt'),
        ('04', 'Pencil Skirt'),
        ('05', 'Pleated Skirt'),
        ('06', 'A-Line Skirt'),
    ]

    TOP_CHOICES = [
        ('00', 'ugly top'),  # for sissies who don't deserve nice tops
        ('01', 'T-Shirt'),
        ('02', 'Blouse'),
        ('03', 'Crop Top'),
        # Add other top types
        ('04', 'Bra'),
        ('05', 'Corset'),
        ('06', 'Bustier'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='sissy_avatar')
    image_path = models.CharField(max_length=200, blank=True, null=True)
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='01')
    skin = models.CharField(
        max_length=10, choices=SKIN_CHOICES, default='light')
    hair = models.CharField(max_length=2, choices=HAIR_CHOICES, default='01')
    hair_color = models.CharField(
        max_length=10, choices=HAIR_COLOR_CHOICES, default='black')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    purchased_items = models.ManyToManyField('Item', blank=True)
    equipped_items = models.ManyToManyField('Item', related_name='equipped_items', blank=True)
    shoes = models.CharField(max_length=100, choices=SHOES_CHOICES, default='00')
    accessories = models.CharField(max_length=100, choices=ACCESSORIES_CHOICES, default='00')
    skirt = models.CharField(max_length=100, choices=SKIRT_CHOICES, default='00')
    top = models.CharField(max_length=100, choices=TOP_CHOICES, default='00')

    def get_image_urls(self):
        """
        Returns a dictionary of image URLs for each avatar component.
        """
        return {
            'body': static(f'dressup/avatars/body/{self.body}/{self.skin}.png'),
            'hair': static(f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png'),
            'shoes': static(f'dressup/avatars/shoes/{self.shoes}.png'),
            'accessories': static(f'dressup/avatars/accessories/{self.accessories}.png'),
            'skirt': static(f'dressup/avatars/skirt/{self.skirt}.png'),
            'top': static(f'dressup/avatars/top/{self.top}.png'),
        }

    def toggle_item(self, item):
        if item in self.equipped_items.all():
            self.equipped_items.remove(item)
            return "unequipped"
        self.equipped_items.add(item)
        return "equipped"
    
    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"
    # Optionally, define methods to get image URLs
    

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
