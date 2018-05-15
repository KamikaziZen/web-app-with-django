from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import SignupForm, LoginForm
from subreddits.models import Subreddit
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import random


def login_signup(request):
    context = {
        'signup_form': SignupForm(),
        'login_form': LoginForm(),
    }
    if request.method == 'GET':
        return render(request, 'core/login.html', context)
    if request.method == 'POST':
        if 'sign_up' in request.POST:
            form = SignupForm(request.POST)
            context['signup_form'] = form
        elif 'log_in' in request.POST:
            form = LoginForm(request.POST)
            context['login_form'] = form
        else:
            return render(request, 'core/login.html', context)
        if form.is_valid(request):
            next_page = request.GET['next']
            # return redirect('mainpage')
            return HttpResponseRedirect(next_page)
        else:
            return render(request, 'core/login.html', context)


@login_required
def logout_view(request):

    previous_page = request.GET['previous']
    logout(request)
    return render(request, 'core/logout.html', {'previous_page': previous_page})


def index(request):

    subscriptions = None
    if request.user.is_authenticated:
        subscriptions = list(request.user.subscriptions.all())
    subreddits = list(Subreddit.objects.all())
    subreddits_display = random.sample(subreddits, 10)
    context = {
        'subreddits_display': subreddits_display,
        'user_subscriptions': subscriptions,
    }
    return render(request, 'core/main.html', context)

