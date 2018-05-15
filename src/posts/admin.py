from django.contrib import admin
from .models import Post, PostVote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = 'title', 'author', 'subreddit', 'created', 'num_comments'
    search_fields = 'title', 'author__username', 'subreddit__name'
    list_filter = 'subreddit',

    def num_comments(self, obj):
        return len([c.author.username for c in obj.comments.all()])


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):

    list_display = 'voter', 'post', 'up',
