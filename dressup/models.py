from django.db import models
from journal.models import CustomUser


class Avatar(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    body = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    hair = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    eyes = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    top = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    bottom = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    shoes = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    accessories = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)



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
