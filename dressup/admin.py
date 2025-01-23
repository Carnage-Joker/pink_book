from django.contrib import admin
from .models import Avatar, Shop, Item, PurchasedItem


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'hair')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price_points', 'premium_only', 'price_dollars')


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'purchased_at', 'used')
