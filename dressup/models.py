from django.db import models
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from journal.models import CustomUser

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
            raise ValueError("Invalid image path: must start with 'dressup/'.")
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
    BODY_CHOICES = (('00', 'Straight'), ('01', 'Petite'),
                    ('02', 'Curvy'), ('03', 'Hourglass'))
    SKIN_CHOICES = (('00', 'Light'), ('01', 'Tan'), ('02', 'Dark'), ('03', 'Ebony'), ('04', 'Albino'), ('05', 'Olive'))
    HAIR_CHOICES = (('h1', 'Short'), ('h2', 'Wavy'), ('h3', 'Long'),('h4', 'Bald'), ('h5', 'Curly'))
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='sissy_avatar')
    name = models.CharField(max_length=100)
    body = models.CharField(max_length=2, choices=BODY_CHOICES, default='00')
    skin = models.CharField(max_length=2, choices=SKIN_CHOICES, default='00')
    hair = models.CharField(max_length=20, choices=HAIR_CHOICES, default='00')
    equipped_items = models.ManyToManyField(
        Item, related_name='equipped_on_avatars', blank=True)

    def get_image_urls(self):
        urls = {
            'body': static(f'dressup/avatars/vectors/svg/{self.skin}/{self.body}.svg'),
            
            'hair': static(f'dressup/avatars/vectors/svg{self.hair}.svg'),
        }
        for item in self.equipped_items.all():
            urls[item.category] = static(item.image_path)
        return urls

    def equip_item(self, item):
        if not item.category:
            raise ValueError("Item must have a category to be equipped.")
        self.equipped_items.filter(category=item.category).delete()
        self.equipped_items.add(item)

    def unequip_item(self, item):
        self.equipped_items.remove(item)

    def __str__(self):
        return f"{self.user.sissy_name}'s Avatar"


class PurchasedItem(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='purchased_items')
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
