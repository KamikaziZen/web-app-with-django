# from unittest import TestCase
from django.test import Client, TestCase
from .models import Subreddit
from posts.models import Post
from core.models import User
from comments.models import Comment
import mock
import faker

import json
import factory


class FakerMock():

    def email(self):
        return "name@yandex.ru"


@mock.patch("faker.Faker", FakerMock)
def fake_email(userObj):
    fake = faker.Faker()
    email_host = fake.email().split('@')[1]
    return "{}@{}".format(userObj.username.lower(), email_host)


class SubredditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subreddit

    name = factory.Faker('last_name')
    about = factory.Faker('sentence', nb_words=4)
    url = factory.LazyAttribute(lambda s: s.name[:4].replace(' ', '').lower())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    is_staff = True
    email = factory.LazyAttribute(fake_email)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    text = factory.Faker('sentence', nb_words=6)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('sentence', nb_words=6)


def get_response_result(response):
    return json.loads(response.getvalue())['result']


class TestApi_create_subreddit(TestCase):

    def setUp(self):
        self.client = Client()
        # Subreddit.objects.create(name='Ethereum', about='about ethereum', url='eth')
        SubredditFactory.create_batch(3)
        poe = SubredditFactory(name='Edgar Allan Poe', url='poe')
        admin = UserFactory()
        post = PostFactory(subreddit=poe, author=admin, title="The Raven")
        CommentFactory.create_batch(5, post=post, author=admin)

    def test_created_objects(self):
        self.logPoint()
        try:
            s = Subreddit.objects.get(url='poe')
        except Exception:
            s = None
        self.assertTrue(s is not None)

    @mock.patch("factory.Faker", autospec=True)
    def test_using_mocking(self, mock_faker):
        self.logPoint()
        factory.Faker('first_name')
        mock_faker.assert_called_with('first_name')


    def test_api_subreddits_list(self):
        self.logPoint()
        request = {
                "jsonrpc" : "2.0",
                "id" : 1,
                "method" : "subreddits.api_subreddits_list"
            }

        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        result = json.loads(get_response_result(response))
        self.assertEqual(len(result), 4)

    def test_api_subreddit(self):
        self.logPoint()
        request = 	{
                    "jsonrpc" : "2.0",
                    "id" : 2,
                    "method" : "subreddits.api_subreddit",
                    "params" : {
                        "url" : "poe"
                    }
                }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        result = json.loads(get_response_result(response))
        # print (result)
        self.assertEqual(result['subreddit_name'], 'Edgar Allan Poe')

    def test_api_create_subreddit(self):
        self.logPoint()
        request = {
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "subreddits.api_create_subreddit",
                        "params": {
                            "name": "Monero",
                            "url": "monero",
                            "about": "about monero"
                        }
                    }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_api_update_subreddit(self):
        self.logPoint()
        about = "American writer, editor, and literary critic."
        request = {
                        "jsonrpc": "2.0",
                        "id": 4,
                        "method": "subreddits.api_update_subreddit",
                        "params": {
                            "name": "Edgar Allan Poe",
                            "url": "poe",
                            "about": about
                        }
                    }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_api_create_post(self):
        self.logPoint()
        request = {
                        "jsonrpc" : "2.0",
                        "id" : 5,
                        "method" : "posts.api_create_post",
                        "params" : {
                            "title" : "Eureka",
                            "text" : "A Prose Poem",
                            "subreddit_url" : "poe"
                        }
                    }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_api_show_comments(self):
        self.logPoint()
        request = {
                        "jsonrpc" : "2.0",
                        "id" : 6,
                        "method" : "comments.api_show_comments",
                        "params" : {
                            "subreddit_url" : "poe",
                            "title" : "The Raven"
                        }
                    }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        result = json.loads(get_response_result(response))
        comments = json.loads(result['comments'])
        print (result)
        self.assertEqual(len(comments), 5)

    def test_api_leave_comment(self):
        self.logPoint()
        request = {
                        "jsonrpc" : "2.0",
                        "id" : 7,
                        "method" : "comments.api_leave_comment",
                        "params" : {
                            "post_title" : "The Raven",
                            "text" : "this is a test comment",
                            "subreddit_url" : "poe"
                        }
                    }
        response = self.client.post('/api/', json.dumps(request), content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        print ("test done")

    def logPoint(self):
        currentTest = self.id().split('.')[-1]
        print ("\non test {}".format(currentTest))
