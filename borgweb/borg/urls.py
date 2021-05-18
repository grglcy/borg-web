from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', cache_page(60)(views.index), name='index'),
    path('post/repo', views.post_repo, name='repo'),
    path('post/archive', views.post_archive, name='archive'),
    path('post/error', views.post_error, name='error'),
    path('post/location', views.post_location, name='location'),
]
