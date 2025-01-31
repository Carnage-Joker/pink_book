from django.contrib import admin
from .models import Avatar, Shop, Item, PurchasedItem


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'skin', 'body', 'hair',)
    list_filter = ('skin', 'body', 'hair',)
    search_fields = ('user__username', 'name')
    actions = ['reset_avatar']

    def reset_avatar(self, request, queryset):
        for avatar in queryset:
            avatar.equipped_items.clear()
            avatar.save()
        self.message_user(request, "Selected avatars have been reset.")


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'shop_type',
                    'premium_only', 'is_locked', 'shop_level')
    list_filter = ('shop_type', 'premium_only')
    search_fields = ('name', 'shop_type')
    actions = ['make_premium_only', 'make_not_premium_only',
               'lock_shops', 'unlock_shops']

    def make_premium_only(self, request, queryset):
        queryset.update(premium_only=True)
        self.message_user(request, "Selected shops are now premium-only.")

    def make_not_premium_only(self, request, queryset):
        queryset.update(premium_only=False)
        self.message_user(
            request, "Selected shops are no longer premium-only.")

    def lock_shops(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected shops are now locked.")

    def unlock_shops(self, request, queryset):
        queryset.update(is_locked=False)
        self.message_user(request, "Selected shops are now unlocked.")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_points',
                    'price_dollars', 'premium_only', 'is_locked')
    list_filter = ('category', 'premium_only')
    search_fields = ('name', 'shop__name')
    actions = ['make_premium_only', 'make_not_premium_only',
               'lock_items', 'unlock_items']

    def make_premium_only(self, request, queryset):
        queryset.update(premium_only=True)
        self.message_user(request, "Selected items are now premium-only.")

    def make_not_premium_only(self, request, queryset):
        queryset.update(premium_only=False)
        self.message_user(
            request, "Selected items are no longer premium-only.")

    def lock_items(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected items are now locked.")

    def unlock_items(self, request, queryset):
        queryset.update(is_locked=False)
        self.message_user(request, "Selected items are now unlocked.")


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'is_equipped')
    list_filter = ('item', 'is_equipped')
    search_fields = ('user__username', 'item__name')
    actions = ['refund_item', 'equip_item', 'unequip_item']

    def refund_item(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected items have been refunded.")

    def equip_item(self, request, queryset):
        for purchased_item in queryset:
            purchased_item.is_equipped = True
            purchased_item.save()
        self.message_user(request, "Selected items have been equipped.")

    def unequip_item(self, request, queryset):
        for purchased_item in queryset:
            purchased_item.is_equipped = False
            purchased_item.save()
        self.message_user(request, "Selected items have been unequipped.")
