from django import template

register = template.Library()


@register.filter
def full_url(subreddit):
    """returns subreddit current url"""
    return subreddit.get_absolute_url()


@register.filter
def get_subscriptions(user):
    return user.subscriptions.all()