from django.contrib import admin
from .models import Comment, CustomUser, JournalEntry, RelatedModel, Report, Quote, Thread, UserProfile, Post, UserFeedback, Tag


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'sissy_name', 'is_staff')
    search_fields = ('email', 'sissy_name')
    list_filter = ('is_staff',)


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'timestamp')
    inlines = [CommentInline,]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'timestamp')
    list_filter = ('author', 'timestamp')
    search_fields = ('content', 'author__sissy_name')
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
