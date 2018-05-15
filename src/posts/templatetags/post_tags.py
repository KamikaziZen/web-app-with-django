from django import template

register = template.Library()

@register.filter
def num_comments(post):
    comments = list(post.comments.all())
    return len(comments)
