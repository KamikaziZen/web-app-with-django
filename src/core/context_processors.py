from subreddits.models import Subreddit
import random
from dumbproject import cache


sample_subreddits = None


def navbar_subs(request):

    sample_subreddits = cache.get('sample_subreddits')
    if sample_subreddits is None:
        sample_subreddits = list(Subreddit.objects.all())
        cache.set('sample_subreddits', sample_subreddits, 3)
    navbar_subreddits = random.sample(sample_subreddits, 20)
    return {'navbar_subreddits' : navbar_subreddits}