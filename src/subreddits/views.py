from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from .models import Subreddit
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from jsonrpc import jsonrpc_method
from django.core.serializers import serialize
import json
from .forms import SubredditApiFormCreate, SubredditApiFormUpdate


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


@jsonrpc_method('subreddits.api_create_subreddit', authenticated=True)
def api_create_subreddit(request, **kwargs):
    # print (request.user)
    # if not request.user.is_authenticated:
    #     raise PermissionDenied("Only authorised users can create new subreddits")
    form = SubredditApiFormCreate(kwargs)
    if not form.is_valid():
        raise ValueError('Form is not valid')
    form.save()
    return "Subreddit /r/{} was successfully submitted".format(kwargs.get('url', ''))


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


@jsonrpc_method('subreddits.api_update_subreddit', authenticated=True)
def api_update_subreddit(request, **kwargs):
    # if not request.user.is_authenticated:
    #     raise PermissionDenied("Only authorised users can update subreddits")
    sub_url = kwargs.get('url', None)
    if not sub_url:
        raise ValueError('Invalid params in request: specify sub_url')
    instance = get_object_or_404(Subreddit, url = sub_url)
    form = SubredditApiFormUpdate(kwargs, instance=instance)
    if form.is_valid():
        form.save()
    return "Subreddit /r/{} has been successfully updated".format(sub_url)


def r(request):

    return redirect('subreddits_list')


def subreddits_list(request):

    context = {
        "subreddits" : Subreddit.objects.all()
    }
    return render(request, "subreddits/subreddits_list.html", context)


@jsonrpc_method('subreddits.api_subreddits_list', authenticated=True)
def api_subreddits_list(request):
    # print (request.user)
    return serialize('json', Subreddit.objects.all())


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


@jsonrpc_method('subreddits.api_subreddit')
def api_subreddit(request, **kwargs):

    context = {}
    sub_url = kwargs.get('url', None)
    if sub_url:
        subreddit = get_object_or_404(Subreddit, url=sub_url)
        # subreddit = Subreddit.objects.get(url=sub_url)
        feed = subreddit.feed.all()
        subscribers = subreddit.subscribers.all()

        context = {
            'subreddit_name': subreddit.name,
            'subreddit_about': subreddit.about,
            'num_posts': len(feed),
            'num_subscribers': len(subscribers),
        }
    return json.dumps(context)


def subredditsListSectionView(request):

    subreddits = Subreddit.objects.annotate(num_subscribers=Count('subscribers'),
                                                  num_posts=Count('feed'))
    return render(request, "subreddits/widgets/subreddit_promo.html", {'subreddits': subreddits.all()})