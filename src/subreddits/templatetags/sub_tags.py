from django import template

register = template.Library()


@register.filter
def full_url(subreddit):
    """returns subreddit current url"""
    return subreddit.get_absolute_url()

@register.filter
def num_subscribers(subreddit):
    subscribers = list(subreddit.subscribers.all())
    return len(subscribers)

@register.filter
def num_posts(subreddit):
    posts = list(subreddit.feed.all())
    return len(posts)

@register.filter
def get_subscriptions(user):
    return user.subscriptions.all()