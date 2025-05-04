from django.contrib import admin
from .models import Item, Shop, Avatar, PurchasedItem, PhotoShoot, LeaderboardEntry


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_points',
                    'price_dollars', 'premium_only', 'is_locked')
    list_filter = ('category', 'premium_only', 'is_locked')
    search_fields = ('name', 'description', 'category')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop_type', 'shop_level',
                    'premium_only', 'is_locked')
    list_filter = ('shop_type', 'shop_level', 'premium_only', 'is_locked')
    search_fields = ('name', 'description')


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'body', 'skin',
                    'hair', 'hair_color', 'story_started')
    list_filter = ('body', 'skin', 'hair_color', 'story_started')
    search_fields = ('name', 'user__sissy_name')


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'purchased_at', 'used', 'is_equipped')
    list_filter = ('used', 'is_equipped')
    search_fields = ('user__sissy_name', 'item__name')


@admin.register(PhotoShoot)
class PhotoShootAdmin(admin.ModelAdmin):
    list_display = ('user', 'photographer_type',
                    'backdrop', 'purchased_at', 'used')
    list_filter = ('photographer_type', 'used')
    search_fields = ('user__sissy_name',)


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('user__sissy_name',)
