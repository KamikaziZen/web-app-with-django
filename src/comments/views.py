from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post
from .models import Comment
import urllib.parse
from .forms import CommentsSortForm, LeaveCommentForm
from django.views.generic import CreateView
from .forms import LeaveCommentForm


def comments(request, sub_url, post_id):

    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
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