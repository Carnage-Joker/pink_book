
from django.contrib import admin
from .models import Comment, CustomUser, JournalEntry, RelatedModel


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
    list_display = ('title', 'user', 'timestamp')  # Updated fields
    inlines = [CommentInline,]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'timestamp')
    list_filter = ('author', 'timestamp')
    search_fields = ('content', 'author__sissy_name')
    actions = ['remove_comment']

    def remove_comment(self, queryset):
        queryset.delete(active=True)
    remove_comment.short_description = "delete selected comments"

@admin.register(RelatedModel)
class RelatedModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_type', 'object_id', 'timestamp')
    list_filter = ('content_type',)

# Register your models here.
