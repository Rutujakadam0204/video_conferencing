from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .routes import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('index', index, name='index'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
