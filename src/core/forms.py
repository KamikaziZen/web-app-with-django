from django import forms
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login, user_login_failed


class SignupForm(forms.Form):

    username = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'choose a username'}))
    password = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'password'}))
    verify_password = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'verify password'}))
    email = forms.CharField(widget=forms.EmailInput
                            (attrs={'placeholder': 'email'}))
    remember_me = forms.BooleanField(label='remember me', required=False)
    email_me = forms.BooleanField(label='email me updates', required=False)

    def is_valid(self, request):

        valid = super(SignupForm, self).is_valid()
        if not valid:
            return valid
        data = self.cleaned_data
        if data['password'] != data['verify_password']:
            self.add_error('password', 'Passwords do not match')
            return False
        else:
            data = self.cleaned_data
            User.objects.create_user(data['username'], data['email'], data['password'])
            return True


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'username'}))
    password = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'password'}))
    remember_me = forms.BooleanField(label='remember me', required=False)

    def is_valid(self, request):

        valid = super(LoginForm, self).is_valid()
        if valid:
            data = self.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'],
                                )
            if user is not None:
                login(request, user)
                return True
            else:
                self.errors['auth failed'] = ': Invalid username or password'
                # self.add_error('myerror', 'Invalid username or password')
                print(self.errors)
                return False