from django.shortcuts import render

from .models import Repo


def index(request):
    repo_list = Repo.objects.all()

    hour_list = [repo.get_archive_hours_dict() for repo in repo_list]
    context = {
        'repo_list': repo_list,
        'hour_list': hour_list
        }
    return render(request, 'borg/index.html', context)
