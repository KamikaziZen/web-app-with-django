from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = 'author', 'post_name', 'num_replies', 'replied_to', 'created'
    search_fields = 'author__username',

    def post_name(self, obj):
        return obj.post.title

    def num_replies(self, obj):
        return len([r for r in obj.replies.all()])

    def replied_to(self, obj):
        return obj.reply_to
