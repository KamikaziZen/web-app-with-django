from django.db import models
from django.contrib.auth.models import AbstractUser
from subreddits.models import Subreddit

class User(AbstractUser):

    subscriptions = models.ManyToManyField(Subreddit,
                                           blank=True,
                                           related_name='subscribers')
    karma = models.IntegerField(default=0)

