from django.db import models
from django.conf import settings
from posts.models import Post
from django.utils import timezone


class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    reply_to = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='replies')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    updated = models.DateTimeField(auto_now=True)

    def __string__(self):
        return '{} on {}'.format(self.author, self.created)

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
        ordering = 'post', 'created', 'id'


class CommentVote(models.Model):

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+')
    up = models.NullBooleanField()