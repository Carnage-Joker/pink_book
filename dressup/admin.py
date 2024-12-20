from django.contrib import admin
from .models import Avatar, Shop, Item, PurchasedItem


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'skin', 'body', 'hair', 'hair_color',)
    list_filter = ('skin', 'body', 'hair', 'hair_color')
    search_fields = ('user__sissy_name', 'name')
    actions = ['reset_avatar']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'shop_type', 'image_path', 'premium_only', 'is_locked', 'shop_level')
    list_filter = ('shop_type', 'premium_only')
    search_fields = ('name', 'shop_type')
    actions = ['make_premium_only', 'make_not_premium_only', 'lock_shops', 'unlock_shops']
    


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_points', 'price_dollars', 'premium_only', 'image_path', 'is_locked')
    list_filter = ('category', 'premium_only')
    search_fields = ('name', 'shop__name')
    actions = ['make_premium_only', 'make_not_premium_only', 'lock_items', 'unlock_items']


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'is_equipped' )
    list_filter = ('item', 'is_equipped')
    search_fields = ('avatar__user__sissy_name', 'item__name')
    actions = ['refund_item', 'equip_item', 'unequip_item', 'mark_as_used', 'mark_as_unused', 'lock_items', 'unlock_items']

