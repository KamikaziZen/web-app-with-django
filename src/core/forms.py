from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    email = forms.EmailField()
    remember_me = forms.BooleanField(label='remember me', required=False)
    email_me = forms.BooleanField(label='email me updates', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    remember_me = forms.BooleanField(label='remember me', required=False)