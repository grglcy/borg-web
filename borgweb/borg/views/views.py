from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from ..models import Repo, Location
from ..utility import data


def index(request):
    repo_list = Repo.objects.all()
    location_list = Location.objects.all()

    context = {
        'repo_list': repo_list,
        'location_list': location_list,
    }
    return render(request, 'borg/index.html', context)


def repo_daily_dict(repo_list, n_days=14):
    date_labels = list(reversed([(datetime.utcnow() - timedelta(days=day)).strftime("%d %b") for day in range(n_days)]))
    max_repo_size = max(repo.latest_archive().cache.unique_csize for repo in repo_list)
    _, max_unit = data.convert_bytes(max_repo_size)

    repo_dicts = [repo.daily_dict(max_unit, n_days) for repo in repo_list]

    return {
        "date_labels": date_labels,
        "repos": repo_dicts,
        "units": max_unit
    }


def repo(request, repo_label: str):
    s_repo = get_object_or_404(Repo, label__label=repo_label)
    return render(request, 'borg/repo.html', {'repo': s_repo})


def axes(request, credentials, *args, **kwargs):
    return render(request, 'error/axes.html', {})
