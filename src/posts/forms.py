from django import forms
from .models import Post, PostVote
from subreddits.models import Subreddit
from django.forms import ValidationError


# class PostForm(forms.ModelForm):
#
#     class Meta:
#         model = Post
#         fields = "title", "text", "subreddit",


class PostVoteForm(forms.ModelForm):

    class Meta:
        model = PostVote
        exclude = 'voter', 'post', 'up',


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=1000)
    subreddit_url = forms.CharField(max_length=50)

    def check_subreddit(self):
        if not Subreddit.objects.get(url=self.subreddit_url):
            raise ValidationError('Form not valid: there is no such subreddit')