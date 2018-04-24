"""dumbproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from core import views as coreviews
from subreddits import views as subviews
from posts import views as postviews
import comments.views as commviews


urlpatterns = [
    path('', coreviews.index, name="mainpage"),
    path('admin/', admin.site.urls),
    path('login/', coreviews.login, name='login'),
    re_path(r'^subreddits/', subviews.subreddits_list, name="subreddits_list"),
    re_path(r'^r/', include('subreddits.urls')),
    re_path(r'^comments/', include('comments.urls'))
]
