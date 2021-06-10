from django.shortcuts import render, get_object_or_404
from ..models import Repo


def index(request):
    repo_list = Repo.objects.all()

    context = {
        'repo_list': repo_list,
    }
    return render(request, 'borg/index.html', context)


def repo(request, repo_label: str):
    s_repo = get_object_or_404(Repo, label__label=repo_label)
    return render(request, 'borg/repo.html', {'repo': s_repo})


def axes(request, credentials, *args, **kwargs):
    return render(request, 'error/axes.html', {})
