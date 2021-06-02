from datetime import datetime, timedelta
from django.http import JsonResponse
from ..models import Repo
from ..utility import data
from ..utility.time import last_day_previous_months


def repo_monthly_json(request, months_ago: int = 12):
    date_labels = [date.strftime("%b %Y") for date in last_day_previous_months(months_ago)]

    repo_list = Repo.objects.all()

    max_unit = get_units(repo_list)

    repo_dicts = [{
        "id": repo.id,
        "label": repo.label.label,
        "size": repo.size_on_months(max_unit, months_ago)
    } for repo in repo_list]

    response_dict = {
        "dates": date_labels,
        "repos": repo_dicts,
        "units": max_unit
    }
    return JsonResponse(response_dict)


def repo_daily_json(request, days_ago: int = 30):
    repo_list = Repo.objects.all()
    dates = [(datetime.utcnow() - timedelta(days=day)) for day in range(days_ago)][::-1]
    return JsonResponse(repo_size_dict(repo_list, dates, "%d %b"))


def repo_size_dict(repo_list, dates: list, date_format: str):
    date_labels = list([day.strftime(date_format) for day in dates])

    max_unit = get_units(repo_list)

    repo_dicts = [{
        "id": repo.id,
        "label": repo.label.label,
        "size": repo.size_on_dates(max_unit, dates)
    } for repo in repo_list]

    return {
        "dates": date_labels,
        "repos": repo_dicts,
        "units": max_unit
    }


def get_units(repo_list):
    max_repo_size = max(repo.latest_archive().cache.unique_csize for repo in repo_list)
    _, max_unit = data.convert_bytes(max_repo_size)
    return max_unit
