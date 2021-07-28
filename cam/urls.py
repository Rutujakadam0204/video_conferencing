from django.contrib import admin
from django.urls import path
# from django.contrib.auth.decorators import login_required
from .views import *
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', index, name=''),
    path('room/<int:room_id>/', room, name='room'),
    path('room/<int:room_id>/ws', room_ws, name='room_ws'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
