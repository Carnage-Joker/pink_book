from django.contrib import admin
from .models import Item, PurchasedItem, Avatar


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'hair', 'eyes', 'top', 'bottom', 'shoes', 'accessories')
    search_fields = ('user__username', 'body', 'hair', 'eyes', 'top', 'bottom', 'shoes', 'accessories')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'premium')
    search_fields = ('category', 'name')
    list_filter = ('category',)


@admin.register(PurchasedItem)
class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    search_fields = ('user__username', 'item__name')
