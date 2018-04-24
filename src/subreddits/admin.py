from django.contrib import admin
from .models import Subreddit


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):

    list_display = 'url', 'name', 'get_subscribers', 'num_posts'
    search_fields = 'name',

    def get_subscribers(self, obj):
        return ", ".join([u.username for u in obj.subscribers.all()])

    def num_posts(self, obj):
        return len([p.title for p in obj.feed.all()])