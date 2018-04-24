from django import template

register = template.Library()


@register.filter
def high_level(value):
    """returns high-level comments(those that are not replies)"""
    return value.filter(reply_to=None)

@register.filter
def all(value):
    """returns high-level comments(those that are not replies)"""
    return value.all()