from django import template

register = template.Library()


@register.filter
def full_url(value):
    """returns subreddit current url"""
    return value.get_absolute_url()