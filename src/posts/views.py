from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.views.generic import CreateView, UpdateView
from .forms import PostForm
from subreddits.models import Subreddit
from .models import Post, PostVote
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from .forms import PostVoteForm
from django.contrib.auth.decorators import login_required
from django.db import models
from jsonrpc import jsonrpc_method
from core.models import User

class PostEdit(UpdateView):

    model = Post
    fields = "title", "text",
    template_name = "subreddits/edit_thread.html"
    sub_url = ''

    def form_valid(self, form):
        if self.request.user == self.object.author or self.request.user.is_superuser  :
            return super(PostEdit, self).form_valid(form)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("comments", kwargs={'sub_url':self.kwargs['sub_url'], 'post_id':self.kwargs['post_id']})


def create_new_thread(request, sub_url):

    subreddits = Subreddit.objects.all()
    subreddits_urls = [x.url for x in subreddits]
    if request.method == "GET":
        form = PostForm()
        return render(request, "subreddits/create_new_thread.html", {"form": form, "subreddits_urls": subreddits_urls})
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subreddit = get_object_or_404(Subreddit, url=data['subreddit_url'])
            # form.create(request.user, subreddit)
            # post = form.save(commit=False)
            post = Post()
            post.title = data['title']
            post.text = data['text']
            post.subreddit = subreddit
            post.author = request.user
            post.save()
            return redirect("subreddit", sub_url=data['subreddit_url'])
        else:
            return render(request, "subreddits/create_new_thread.html", {"form": form, "subreddits_urls": subreddits_urls})


@jsonrpc_method('posts.api_create_post', authenticated=True)
def api_create_post(request, **kwargs):

    # if not request.user.is_authenticated:
    #     raise PermissionDenied("Only authorised users can create new posts")
    form = PostForm(kwargs)
    if form.is_valid():
        post = Post()
        post.title = form.cleaned_data['title']
        post.text = form.cleaned_data['text']
        post.subreddit = Subreddit.objects.get(url=form.cleaned_data['subreddit_url'])
        # post.author = request.user
        post.author = User.objects.get(pk=1)
        post.save()
        return "Post {} in subreddit /r/{} has been successfully created"\
            .format(form.cleaned_data['title'], form.cleaned_data['subreddit_url'])


# def edit_thread(request, sub_url, post_id):
#
#     post = get_object_or_404(Post, id=post_id, author=request.user)
#     if request.method == "GET":
#         form = PostForm(instance=post)
#         return render(request, "subreddits/edit_thread.html", {"form": form})
#     elif request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             return redirect("subreddit", sub_url=sub_url)
#         else:
#             return render(request, "subreddits/edit_thread.html", {"form": form})


def simplePostScore(request, sub_url, post_id):

    post = Post.objects.get(id=post_id)
    # postvotes = list(PostVote.objects.filter(post_id=post_id))
    return HttpResponse('<span id=post_score>' + str(post.score) + '</span>')


# class PostVoteView(CreateView):
#
#     model = PostVote
#     form_class = PostVoteForm
#     template_name = 'posts/postvote.html'
#
#     def form_valid(self, form):
#         form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
#         form.instance.voter = self.request.user
#         return super(PostVoteView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("subreddit", kwargs={'sub_url': self.kwargs['sub_url']})


@login_required
def postVoteView(request, sub_url, post_id):

    if request.method == "GET":
        form = PostVoteForm()
        return render(request, "posts/postvote.html", {"form": form})
    elif request.method == "POST":
        form = PostVoteForm(request.POST)
        if form.is_valid():
            if request.user not in [vote.voter for vote in PostVote.objects.filter(post_id=post_id)]:
                post = get_object_or_404(Post, id=post_id)
                # form.create(request.user, subreddit)
                postvote = form.save(commit=False)
                postvote.post = post
                postvote.voter = request.user
                postvote.up = True
                postvote.save()
                Post.objects.filter(id=post_id).update(score=models.F('score')+1)
                return redirect("subreddit", sub_url=sub_url)
            else:
                raise PermissionDenied
        else:
            return render(request, "posts/postvote.html", {"form": form})


def postListView(request, sub_url):

    feed = Subreddit.objects.get(url=sub_url).feed.all()
    # feed = Subreddit.objects.get(url=sub_url).feed.select_related('comments').all()
    return render(request, "posts/widgets/post_promo.html", {'feed': feed})