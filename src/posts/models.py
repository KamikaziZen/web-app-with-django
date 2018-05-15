from django.db import models
from django.conf import settings
from subreddits.models import Subreddit


class Post(models.Model):

    title = models.CharField(max_length=255)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE, related_name='feed')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    score = models.IntegerField(default=0)
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '[{}]: {}'.format(self.author, self.title)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = 'subreddit', 'created', 'id'


class PostVote(models.Model):

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', db_index=True)
    up = models.NullBooleanField()