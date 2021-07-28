from django.contrib import admin
from django.urls import path
# from django.contrib.auth.decorators import login_required
# from rest_framework.urlpatterns import format_suffix_patterns
from . views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', main_view, name='main_view'),
]

