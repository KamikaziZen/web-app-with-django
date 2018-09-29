from .models import Subreddit
from django.forms import ModelForm, ValidationError


class SubredditApiFormCreate(ModelForm):
    class Meta:
        model = Subreddit
        fields = "name", "url", "about",

    def check_unique_url(self):
        sub_url = self.cleaned_data['url']
        if Subreddit.objects.get(url=sub_url):
            raise ValidationError("Subreddit with same url already exists")


class SubredditApiFormUpdate(ModelForm):
    class Meta:
        model = Subreddit
        fields = "name", "url", "about",

    def check_exists_url(self):
        sub_url = self.cleaned_data['url']
        if not Subreddit.objects.filter(url=sub_url):
            raise ValidationError("Subreddit with this url doesn't exist")