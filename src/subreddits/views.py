from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Subreddit


def r(request):

    return redirect('subreddits_list')

def subreddits_list(request):

    context = {
        "subreddits" : Subreddit.objects.all()
    }
    return render(request, "subreddits/subreddits_list.html", context)


def subreddit(request, sub_url):

    subreddit = get_object_or_404(Subreddit, url=sub_url)
    context = {
        'subreddit' : subreddit,
        'feed' : subreddit.feed.all(),
    }
    return render(request, "subreddits/subreddit.html", context)