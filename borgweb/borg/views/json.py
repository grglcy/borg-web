from datetime import datetime, timedelta
from django.http import JsonResponse
from ..models import Repo
from ..utility import data


def repo_daily_dict(repo_list, n_days=14):
    dates = [(datetime.utcnow() - timedelta(days=day)) for day in range(n_days)][::-1]
    date_labels = list([day.strftime("%d %b") for day in dates])

    max_repo_size = max(repo.latest_archive().cache.unique_csize for repo in repo_list)
    _, max_unit = data.convert_bytes(max_repo_size)

    repo_dicts = [repo.size_on_dates(max_unit, dates) for repo in repo_list]

    return {
        "dates": date_labels,
        "repos": repo_dicts,
        "units": max_unit
    }


def repo_daily_json(request):
    repo_list = Repo.objects.all()
    return JsonResponse(repo_daily_dict(repo_list, 31))
