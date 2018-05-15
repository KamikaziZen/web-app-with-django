from django import template

register = template.Library()

@register.filter
def get_posts(subreddit):
    posts = list(subreddit.feed.all())
    return posts