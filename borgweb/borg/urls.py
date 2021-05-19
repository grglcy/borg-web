from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', cache_page(60)(views.index), name='index'),
    path('repo_daily.json', cache_page(3600)(views.repo_daily_json), name='repo json'),
    path('repo/<str:repo_label>', views.repo, name='repo'),
    path('post/repo', views.post_repo, name='post repo'),
    path('post/archive', views.post_archive, name='post archive'),
    path('post/error', views.post_error, name='post error'),
    path('post/location', views.post_location, name='post location'),
]
