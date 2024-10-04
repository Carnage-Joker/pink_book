from django.db import models
from journal.models import CustomUser
from django.conf import settings


class Avatar(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.ImageField(upload_to='avatars/body/', max_length=100, null=True, blank=True)
    hair = models.ImageField(upload_to='avatars/hair/', max_length=100, null=True, blank=True)
    eyes = models.ImageField(upload_to='avatars/eyes/', max_length=100, null=True, blank=True)
    top = models.ImageField(upload_to='avatars/top/', max_length=100, null=True, blank=True)
    bottom = models.ImageField(upload_to='avatars/bottom/', max_length=100, null=True, blank=True)
    shoes = models.ImageField(upload_to='avatars/shoes/', max_length=100, null=True, blank=True)
    accessories = models.ImageField(
        upload_to='avatars/accessories/', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories')
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.BooleanField(default=False)


class PurchasedItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
