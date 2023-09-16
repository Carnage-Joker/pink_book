from django.contrib import admin
from .models import RelatedModel, Comment, CustomUser, JournalEntry

admin.site.register(JournalEntry)
admin.site.register(CustomUser)
admin.site.register(RelatedModel)  # Register RelatedModel without any inlines

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'content_type', 'object_id']
    list_filter = ['content_type']

# You can add more admin registrations for other models if needed


