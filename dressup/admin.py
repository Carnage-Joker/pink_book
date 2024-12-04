from django.contrib import admin

# dressup/admin.py

from django.contrib import admin
from .models import Avatar, Shop, Item, PurchasedItem


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'skin', 'body', 'hair')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price')


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('avatar', 'item', 'purchase_date')
