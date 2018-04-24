from django.contrib import admin
from django.urls import path, include, re_path
import comments.views as commvies

urlpatterns = [
    path('<int:post_id>/', commvies.by_id, name="comments_by_id"),
    path('<int:post_id>/<str:post_url>/', commvies.comments, name="comments"),
]