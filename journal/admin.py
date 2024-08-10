
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import (BlogPost, Comment, CustomUser, Faq, JournalEntry, Post, Quote,
                     RelatedModel, Report, Tag, Thread, UserFeedback,
                     UserProfile)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'sissy_name', 'is_active',
                    'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'activate_account_token')}),
        ('Personal info', {'fields': ('sissy_name', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'sissy_type', 'sissy_name')
    ordering = ('email',)
    filter_horizontal = ()
    actions = ['deactivate_users', 'activate_users']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp')
    search_fields = ('title', 'author__sissy_name')
    list_filter = ('timestamp',)
    
    # list_editable = ('title', 'author', 'timestamp')  
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'timestamp')
    search_fields = ('title', 'user__sissy_name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content',)
    actions = ['remove_comment']

    def remove_comment(self, request, queryset):
        queryset.delete()
    remove_comment.short_description = "Delete selected comments"


@admin.register(RelatedModel)
class RelatedModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_type', 'object_id', 'timestamp')
    list_filter = ('content_type',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'reason', 'reported_by', 'timestamp')
    search_fields = ('reason', 'reported_by__sissy_name')
    list_filter = ('timestamp',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'timestamp')
    search_fields = ('content', 'author')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'privacy_level', 'nsfw_blur', 'insight_opt')
    search_fields = ('user__sissy_name',)
    list_filter = ('privacy_level',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp')
    search_fields = ('title', 'author__sissy_name',)
    list_filter = ( 'timestamp',)


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('user__sissy_name', 'content')
    list_filter = ('timestamp',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question', 'answer')
    list_filter = ('question', 'answer')
    actions = ['remove_faq']

    def remove_faq(self, request, queryset):
        queryset.delete()
    remove_faq.short_description = "Delete selected faqs"