from django.db import models
from django.shortcuts import reverse


class Subreddit(models.Model):
    name = models.CharField(max_length=255)
    about = models.CharField(max_length=500)
    url = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return '{}: {}\nAbout: {}'.format(self.get_absolute_url(), self.name, self.about)

    def get_absolute_url(self):
        return reverse("subreddit", kwargs={'sub_url' : self.url})[1:]

    class Meta:
        verbose_name = 'Subreddit'
        verbose_name_plural = 'Subsreddits'
        ordering = 'url', 'id'