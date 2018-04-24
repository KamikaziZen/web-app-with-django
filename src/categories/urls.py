from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from categories.views import category_detail, category_list

urlpatterns = [
    path('', category_list),
    re_path(r'^(\d+)/$', category_detail, name='category_detail')
]