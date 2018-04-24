from django.shortcuts import render, HttpResponse
from .forms import SignupForm, LoginForm
from .models import User


def get_user_data(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User()
            u.username = form.username
            u.password = form.password
            u.email = form.email
            u.save()
            return render(request, 'core/main.html')

    else:
        context = {
            'signup_form' : SignupForm(),
            'login_form' : LoginForm(),
        }
        return render(request, 'core/login.html', context)


def index(request):

    return render(request, 'core/main.html')


def login(request):

    signup = SignupForm(request.POST)
    login = LoginForm(request.POST)
    context = {
        'signup_form' : signup,
        'login_form' : login,
    }
    return render(request, 'core/login.html', context)

