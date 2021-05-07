from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('repo', views.get_repo, name='repo'),
    path('archive', views.get_archive, name='archive'),
]
