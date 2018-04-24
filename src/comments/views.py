from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
import urllib.parse
from django import forms

class CommentsForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('-score', 'best'),
        ('-created', 'new'),
        ('created', 'old'),
    ), required=False)


def comments(request, post_id, post_url):

    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentsForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            comments = comments.order_by(data['sort'])
    context = {
        'post' : post,
        'comments' : comments,
        'comments_form' : form,
    }
    return render(request, "comments/comments.html", context)


def by_id(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    return redirect("comments",
                    post_id=post_id,
                    post_url=urllib.parse.quote_plus(post.title))