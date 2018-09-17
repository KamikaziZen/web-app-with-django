from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from .models import Subreddit
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db.models import Count


class CreateSubreddit(CreateView):

    model = Subreddit
    fields = "name", "url", "about",
    template_name = "subreddits/create_new_subreddit.html"
    sub_url = ''

    def form_valid(self, form):
        self.sub_url = form.instance.url
        if self.request.user.id == 1:
            return super(CreateSubreddit, self).form_valid(form)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("subreddit", kwargs={'sub_url': self.sub_url})


class UpdateSubreddit(UpdateView):

    model = Subreddit
    fields = "name", "url", "about",
    template_name = "subreddits/edit_subreddit.html"
    sub_url = ''

    def get_object(self, queryset=None):
        return Subreddit.objects.get(url=self.kwargs['sub_url'])

    def form_valid(self, form):
        self.sub_url = form.instance.url
        if self.request.user.id == 1:
            return super(UpdateSubreddit, self).form_valid(form)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("subreddit", kwargs={'sub_url': self.sub_url})


def r(request):

    return redirect('subreddits_list')


def subreddits_list(request):

    context = {
        "subreddits" : Subreddit.objects.all()
    }
    return render(request, "subreddits/subreddits_list.html", context)


def subreddit(request, sub_url):

    # subreddit = get_object_or_404(Subreddit.objects.prefetch_related('feed__comments','feed__author'),
    #                               url=sub_url)
    subreddit = get_object_or_404(Subreddit, url=sub_url)
    feed = subreddit.feed.all().select_related('author').prefetch_related('comments')

    context = {
        'subreddit' : subreddit,
        'feed' : feed,
    }
    return render(request, "subreddits/subreddit.html", context)

def subredditsListSectionView(request):

    subreddits = Subreddit.objects.annotate(num_subscribers=Count('subscribers'),
                                                  num_posts=Count('feed'))
    return render(request, "subreddits/widgets/subreddit_promo.html", {'subreddits': subreddits.all()})