from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post
from subreddits.models import Subreddit
from .models import Comment
import urllib.parse
from .forms import CommentsSortForm, LeaveCommentForm, LeaveCommentApiForm
from django.views.generic import CreateView
from jsonrpc import jsonrpc_method
import json
from django.core.serializers import serialize
from core.models import User


def comments(request, sub_url, post_id):

    post = get_object_or_404(Post.objects.select_related('subreddit', 'author'), id=post_id)
    comments = post.comments.select_related('author').prefetch_related('replies').all()
    comments_sort_form = CommentsSortForm()
    if request.method == "GET":
        comments_sort_form = CommentsSortForm(request.GET)
        if comments_sort_form.is_valid():
            data = comments_sort_form.cleaned_data
            if data['sort']:
                comments = comments.order_by(data['sort'])
    elif request.method == "POST":
        leave_comment_form = LeaveCommentForm(request.POST)
        if leave_comment_form.is_valid():
            data = leave_comment_form.cleaned_data
            c = Comment()
            c.post = post
            c.author = request.user
            c.text = data['text']
            c.save()
            comments = post.comments.all()
    leave_comment_form = LeaveCommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comments_sort_form': comments_sort_form,
        'leave_comment_form': leave_comment_form,
        'sub_url': sub_url,
    }
    return render(request, "comments/comments.html", context)


@jsonrpc_method('comments.api_show_comments', authenticated=True)
def api_show_comments(request, **kwargs):

    sub_url = kwargs.get('subreddit_url', None)
    if not sub_url:
        raise ValueError("Error in params: specify subreddit_url")
    title = kwargs.get('title', None)
    if not title:
        raise ValueError("Error in params: specify post title")
    subreddit = Subreddit.objects.get(url=sub_url)
    if not subreddit:
        raise ValueError("There is no subreddit with such url")
    posts = Post.objects.filter(subreddit=subreddit, title=title).prefetch_related('comments')
    context = {}
    for idx, post in enumerate(posts):
        context[idx] = {
            "title" : post.title,
            "text" : post.text,
            "author" : post.author.username,
            "comments" : serialize('json', post.comments.all())
        }
    return json.dumps(context)


def by_id(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    return redirect("comments",
                    post_id=post_id,
                    post_url=urllib.parse.quote_plus(post.title))


def comments_contents(request, sub_url, post_id):

    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    context = {
        'comments': comments,
    }
    return render(request, 'comments/comments_contents.html', context)


class CreateComment(CreateView):

    model = Comment
    form_class = LeaveCommentForm
    template_name = "comments/create_new_comment.html"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.post_id=self.kwargs['post_id']
        return super(CreateComment, self).form_valid(form)

    def get_success_url(self):
        return reverse("comments", kwargs={'sub_url': self.kwargs['sub_url'], 'post_id': self.kwargs['post_id']})


@jsonrpc_method('comments.api_leave_comment', authenticated=True)
def api_leave_comment(request, **kwargs):

    form = LeaveCommentApiForm(kwargs)
    if not form.is_valid():
        raise ValueError('Form is not valid')
    comment = Comment()
    comment.author = User.objects.get(pk=1)
    comment.text = form.cleaned_data['text']
    subreddit = Subreddit.objects.prefetch_related('feed').get(url=form.cleaned_data['subreddit_url'])
    post = subreddit.feed.get(title=form.cleaned_data['post_title'])
    comment.post = post
    comment.save()
    return "Your comment in post {} subreddit /r/{} has been successfully submitted"\
        .format(form.cleaned_data['post_title'], form.cleaned_data['subreddit_url'])