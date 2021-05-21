from datetime import datetime, timedelta
from django.http import JsonResponse
from ..models import Repo
from ..utility import data


def repo_daily_dict(repo_list, n_days=14):
    date_labels = list(reversed([(datetime.utcnow() - timedelta(days=day)).strftime("%d %b") for day in range(n_days)]))
    max_repo_size = max(repo.latest_archive().cache.unique_csize for repo in repo_list)
    _, max_unit = data.convert_bytes(max_repo_size)

    repo_dicts = [repo.daily_dict(max_unit, n_days) for repo in repo_list]

    return {
        "dates": date_labels,
        "repos": repo_dicts,
        "units": max_unit
    }

def repo_daily_json(request):
    repo_list = Repo.objects.all()
    return JsonResponse(repo_daily_dict(repo_list, 31))
