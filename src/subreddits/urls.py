from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from subreddits import views as subviews

urlpatterns = [
    path('', subviews.r),
    path('<slug:sub_url>/', subviews.subreddit, name="subreddit"),

]