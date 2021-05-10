from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/repo', views.get_repo, name='repo'),
    path('post/archive', views.get_archive, name='archive'),
    path('post/error', views.get_error, name='error'),
]
