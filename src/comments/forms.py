from django import forms
from .models import Comment, CommentVote


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

