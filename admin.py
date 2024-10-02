from django.contrib import admin
from .models import CustomUser, Billing, JournalEntry, Habit, ToDo, Thread, Post, Comment, SubscriptionTier


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('sissy_name', 'email', 'subscription_tier',
                    'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'sissy_name')
    list_filter = ('subscription_tier', 'is_active', 'is_staff')
    ordering = ('date_joined',)

    def subscription_tier(self, obj):
        return obj.subscription_tier
    subscription_tier.short_description = 'Subscription Tier'


admin.site.register(CustomUser, CustomUserAdmin)


class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_tier',
                    'status', 'created_at', 'updated_at')
    list_filter = ('subscription_tier', 'status')


admin.site.register(Billing, BillingAdmin)


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'timestamp', 'insight')
    list_filter = ('user__subscription_tier', 'timestamp')
    search_fields = ('title', 'content')


admin.site.register(JournalEntry, JournalEntryAdmin)


class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'increment_counter')
    list_filter = ('user__subscription_tier', 'created_at')
    search_fields = ('name',)


admin.site.register(Habit, HabitAdmin)


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'due_date', 'completed')
    list_filter = ('user__subscription_tier', 'due_date', 'completed')
    search_fields = ('title',)


admin.site.register(ToDo, ToDoAdmin)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


admin.site.register(Thread, ThreadAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'title', 'author', 'timestamp')
    list_filter = ('thread__title', 'author__subscription_tier', 'timestamp')
    search_fields = ('title', 'content')


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'timestamp')
    list_filter = ('author__subscription_tier', 'timestamp')
    search_fields = ('content',)


admin.site.register(Comment, CommentAdmin)


class SubscriptionTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)


admin.site.register(SubscriptionTier, SubscriptionTierAdmin)
