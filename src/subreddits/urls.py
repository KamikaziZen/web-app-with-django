from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from subreddits import views as subviews
from posts import views as postviews
from comments import views as commviews
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', subviews.r),
    path('create_new_subreddit/',
         login_required(subviews.CreateSubreddit.as_view()),
         name="create_new_subreddit"),
    path('<slug:sub_url>/', subviews.subreddit, name="subreddit"),
    path('<slug:sub_url>/<int:post_id>/score/', postviews.simplePostScore, name="simplePostScore"),
    path('<slug:sub_url>/comments/<int:post_id>/contents/', commviews.comments_contents, name="comments_contents"),
    path('edit/<slug:sub_url>/',
         login_required(subviews.UpdateSubreddit.as_view()),
         name="edit_subreddit"),
    path('<slug:sub_url>/edit/<int:post_id>/',
         login_required(postviews.PostEdit.as_view(pk_url_kwarg='post_id')),
         name="edit_thread"),
    path('<slug:sub_url>/comments/<int:post_id>/', commviews.comments, name="comments"),
    path('<slug:sub_url>/create_new_thread/',
         login_required(postviews.create_new_thread),
         name="create_new_thread"),
    path('<slug:sub_url>/comments/<int:post_id>/create_new_comment/',
             login_required(commviews.CreateComment.as_view()),
             name="create_new_comment"),
    path('<slug:sub_url>/<int:post_id>/score_up/',
            postviews.postVoteView,
            name="PostUpButton"),
    path('subredditslistcontents',
         subviews.subredditsListSectionView,
         name="SubredditListContents"),
]