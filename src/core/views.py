from django.shortcuts import render, HttpResponse
from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    email = forms.EmailField()
    remember_me = forms.BooleanField(label='remember me')
    email_me = forms.BooleanField(label='email me updates')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    remember_me = forms.BooleanField(label='remember me')


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

