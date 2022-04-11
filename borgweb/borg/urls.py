from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # Index Page
    path('', cache_page(60)(views.index), name='index'),

    path('repo-list.json', cache_page(60)(views.repo_list_json), name='repo list'),

    # Repo
    path('repo/<str:repo_label>/monthly-size.json', cache_page(3600)(views.repo_monthly_size_json),
         name='repo size time series'),
    path('repo/<str:repo_label>.json', cache_page(60)(views.repo_json), name='repo json'),
    path('repo/<str:repo_label>/latest-backup.json', cache_page(60)(views.repo_latest_backup_json), name='repo json'),
    path('repo/<str:repo_label>/size.json', cache_page(60)(views.repo_size_json), name='repo size json'),
    path('repo/<str:repo_label>/recent-errors.json', cache_page(60)(views.repo_recent_errors_json),
         name='repo recent errors json'),

    # Repo page
    path('repo/<str:repo_label>', cache_page(60)(views.repo), name='repo'),

    # POST
    path('post/repo', views.post_repo, name='post repo'),
    path('post/archive', views.post_archive, name='post archive'),
    path('post/error', views.post_error, name='post error'),
    path('post/location', views.post_location, name='post location'),

    # Unused
    path('repo_daily.json', cache_page(3600)(views.repo_daily_json), name='daily repo json'),
    path('repo_monthly.json', cache_page(3600 * 12)(views.repo_monthly_json), name='monthly repo json'),
]
