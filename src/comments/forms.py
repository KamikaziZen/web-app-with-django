from django import forms
from .models import Comment, CommentVote
from subreddits.models import Subreddit
from posts.models import Post
from django.forms import ValidationError


class CommentsSortForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('-score', 'best'),
        ('-created', 'new'),
        ('created', 'old'),
    ), required=False)


class LeaveCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude=['post', 'author', 'reply_to', 'score']


class LeaveCommentApiForm(forms.Form):
    post_title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=1000)
    subreddit_url = forms.CharField(max_length=50)

    def check_post(self):
        subreddit = Subreddit.objects.prefetch_related('feed').get(url=self.subreddit_url)
        if not subreddit.feed.get(subreddit=subreddit, title=self.post_title):
            raise ValidationError("There is no post with this title in this subreddit")

