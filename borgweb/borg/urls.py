from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', cache_page(60)(views.index), name='index'),
    path('repo_daily.json', cache_page(3600)(views.repo_daily_json), name='daily repo json'),
    path('repo_monthly.json', cache_page(3600 * 12)(views.repo_monthly_json), name='monthly repo json'),
    path('repo_list.json', cache_page(3600)(views.repo_list), name='repo list'),
    path('repo/<str:repo_label>', cache_page(60)(views.repo), name='repo'),
    path('post/repo', views.post_repo, name='post repo'),
    path('post/archive', views.post_archive, name='post archive'),
    path('post/error', views.post_error, name='post error'),
    path('post/location', views.post_location, name='post location'),
]
