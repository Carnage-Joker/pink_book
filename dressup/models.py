# dressup/models.py
from operator import is_
from django.contrib.auth import get_user_model
from journal.models import CustomUser  # Replace 'your_app' with the actual app name
from django.templatetags.static import static  # Import static
from django.db import models


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
    )

    name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_path = models.CharField(max_length=200, blank=True, null=True)
    price_points = models.IntegerField(default=0, blank=True, null=True)
    price_dollars = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    premium_only = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(blank=True)

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
        # Add more shop types as needed
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
        return static(f'dressup/shops/{self.shop_level}/{self.image_path}')

    def __str__(self):
        return self.name


User = get_user_model()


class Avatar(models.Model):
    # Choice Tuples
    BODY_CHOICES = (
        ('00', 'straight_body'),
        ('01', 'petite_body'),
        ('02', 'curvy_body'),
        ('03', 'hourglass_body'),
        ('04', 'pear_body'),
        ('05', 'apple_body'),
        ('06', 'athletic_body'),
        # Add more body types as needed
    )
    SKIN_CHOICES = (
        ('00', 'light'),
        ('01', 'olive'),
        ('02', 'medium'),
        ('03', 'dark'),
        ('04', 'pale'),
        ('05', 'tan'),
    )
    HAIR_CHOICES = (
        ('00', 'short_hair'),
        ('01', 'short_wavy_bangs'),
        ('02', 'long_straight_hair'),
        ('03', 'long_curly_hair'),
        ('04', 'long_wavy_hair'),
        ('05', 'bob_cut'),
        ('06', 'pig_tails'),
        ('07', 'bald'),
        ('08', 'short_curly_hair'),
        ('09', 'short_wavy_hair'),
        ('10', 'long_straight_bangs'),
        ('11', 'long_curly_bangs'),
        ('12', 'long_wavy_bangs'),
        ('13', 'bob_cut_bangs'),
        ('14', 'pig_tails_bangs'),
        ('15', 'short_curly_bangs'),
        # Add more hair styles as needed
    )
    HAIR_COLOR_CHOICES = (
        ('00', 'none'),  # for wigs
        ('black', 'black'),
        ('brunette', 'brown'),
        ('blonde', 'blonde'),
        ('red', 'red'),
        ('pink', 'pink'),
    )

    SHOES_CHOICES = [
        ('00', 'Basic Shoes'),
        ('01', 'Sneakers'),
        ('02', 'Boots'),
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
        ('03', 'Gloves'),
        ('04', 'Sunglasses'),
        ('05', 'Handbag'),
        ('06', 'Necklace'),
        ('07', 'Bracelet'),
        ('08', 'Earrings'),
        ('09', 'Collar'),
        ('10', 'Belt'),
    ]

    SKIRT_CHOICES = [
        ('00', 'Basic Shorts'),
        ('01', 'Mini Skirt'),
        ('02', 'Midi Skirt'),
        ('03', 'Maxi Skirt'),
        ('04', 'Pencil Skirt'),
        ('05', 'Pleated Skirt'),
        ('06', 'A-Line Skirt'),
    ]

    TOP_CHOICES = [
        ('00', 'Basic Top'),
        ('01', 'T-Shirt'),
        ('02', 'Blouse'),
        ('03', 'Crop Top'),
        ('04', 'Bra'),
        ('05', 'Corset'),
        ('06', 'Bustier'),
    ]

    # Model Fields
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='sissy_avatar')
    name = models.CharField(max_length=100)
    image_path = models.CharField(
        max_length=200, blank=True, null=True)  # Optional: If used
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=20, choices=HAIR_CHOICES, default='00')
    hair_color = models.CharField(
        max_length=20, choices=HAIR_COLOR_CHOICES, default='00')
    shoes = models.CharField(max_length=2, choices=SHOES_CHOICES, default='00')
    accessories = models.CharField(
        max_length=2, choices=ACCESSORIES_CHOICES, default='00')
    skirt = models.CharField(max_length=2, choices=SKIRT_CHOICES, default='00')
    top = models.CharField(max_length=2, choices=TOP_CHOICES, default='00')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    purchased_items = models.ManyToManyField(
        'Item', blank=True)  # Ensure Item model is defined
    equipped_items = models.ManyToManyField(
        'Item',
        related_name='equipped_on_avatars',
        blank=True,
        help_text="Items currently equipped on the avatar."
    )

    def equip_item(self, item):
        """
        Equip an item to the avatar, ensuring only one item per category is equipped.
        """
        if item.category:
            # Remove currently equipped item of the same category
            self.equipped_items.filter(category=item.category).delete()
        # Equip the new item
        self.equipped_items.add(item)
        self.save()

    def unequip_item(self, item):
        """
        Unequip an item from the avatar.
        """
        self.equipped_items.remove(item)
        self.save()

    def get_image_urls(self):
        """
        Returns a dictionary of image URLs for each avatar component.
        Dynamically checks equipped items to build the URLs.
        """
        urls = {
            'body': (f'dressup/avatars/body/{self.skin}/{self.body}.png'),
            'hair': (f'dressup/avatars/hair/{self.hair}/{self.hair_color}.png'),
            'shoes': (f'dressup/avatars/shoes/{self.shoes}.png'),
            'accessories': (f'dressup/avatars/accessories/{self.accessories}.png'),
            'skirt': (f'dressup/avatars/skirts/{self.skirt}.png'),
            'top': (f'dressup/avatars/tops/{self.top}.png'),
        }
        # Add URLs for equipped items
        for item in self.equipped_items.all():
            urls[item.category] = item.image_path

        return urls
        # Optionally, define methods to get image URLs
        

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
    # For one-time use items like photoshoots
    used = models.BooleanField(default=False)
    is_equipped = models.BooleanField(default=False)

    def __str__(self):
        # Also using 'sissy_name' if your CustomUser has it:
        return f"{self.user.sissy_name} purchased {self.item.name}"


class PhotoShoot(models.Model):
    PHOTOGRAPHER_CHOICES = (
        ('booth', 'Photo Booth'),
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
