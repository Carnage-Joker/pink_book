from .models import Avatar, ClothingItem, FavoriteOutfit, PhotoshootLocation, Item, PurchasedItem
from django.contrib import admin


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'hair', 'eyes', 'top', 'bottom', 'shoes', 'accessories')
    search_fields = ('user__username', 'body', 'hair', 'eyes', 'top', 'bottom', 'shoes', 'accessories')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'is_premium')
    search_fields = ('category', 'name')
    list_filter = ('category',)


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    search_fields = ('user__username', 'item__name')


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_premium')
    list_filter = ('type', 'is_premium')
    search_fields = ('name',)


@admin.register(FavoriteOutfit)
class FavoriteOutfitAdmin(admin.ModelAdmin):
    list_display = ('user', 'outfit_name')
    filter_horizontal = ('clothing_items',)


@admin.register(PhotoshootLocation)
class PhotoshootLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_premium')
    search_fields = ('name',)
