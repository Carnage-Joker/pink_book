from django.contrib import admin
from .models import Avatar, PremiumOutfit, Pose, Environment, Feature, Favorites


@admin.register(Pose)
class PoseAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name',)

    def image_preview(self, obj):
        return obj.image and '<img src="{}" width="50" height="50" />'.format(obj.image.url)
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name',)

    def image_preview(self, obj):
        return obj.image and '<img src="{}" width="50" height="50" />'.format(obj.image.url)
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


@admin.register(PremiumOutfit)
class PremiumOutfitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview')
    search_fields = ('name', 'price')
    list_filter = ('price',)

    def image_preview(self, obj):
        return obj.image and '<img src="{}" width="50" height="50" />'.format(obj.image.url)
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'body_type', 'skin_tone',
                    'hair_style', 'hair_color')
    search_fields = ('user__username', 'body_type',
                     'skin_tone', 'hair_style', 'hair_color')
    list_filter = ('body_type', 'skin_tone', 'hair_style', 'hair_color')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'image_url')
    search_fields = ('category', 'name')
    list_filter = ('category',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'outfit', 'created_at')
    search_fields = ('user__username', 'outfit__name')
    list_filter = ('created_at',)

# Inline models (if you want to show related models within the same admin page)


class FavoritesInline(admin.TabularInline):
    model = Favorites
    extra = 1

# Registering models with inline (if required)


class UserAdmin(admin.ModelAdmin):
    inlines = [FavoritesInline]
