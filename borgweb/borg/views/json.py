from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import Repo, Label
from ..utility import data
from ..utility.time import last_day_previous_months


def repo_json(request, repo_label):
    repo = get_object_or_404(Repo, label__label=repo_label)
    repo_dict = {'warning': repo.warning(),
                 'error': repo.error()}
    return JsonResponse(repo_dict)


def repo_latest_backup_json(request, repo_label):
    repo = get_object_or_404(Repo, label__label=repo_label)
    return JsonResponse({"data": repo.last_backup()})


def repo_size_json(request, repo_label):
    repo = get_object_or_404(Repo, label__label=repo_label)
    return JsonResponse({"data": repo.size_string()})


def repo_recent_errors_json(request, repo_label):
    repo = get_object_or_404(Repo, label__label=repo_label)
    return JsonResponse({"data": len(repo.recent_errors())})


def repo_monthly_size_json(request, repo_label, months_ago: int = 12):
    repo = get_object_or_404(Repo, label__label=repo_label)

    date_labels = [date.strftime("%b %Y") for date in last_day_previous_months(months_ago)]

    max_unit = get_units([repo])

    repo_dict = {"id": repo.id,
                 "label": repo.label.label,
                 "size": repo.size_on_months(max_unit, months_ago)}

    response_dict = {
        "dates": date_labels,
        "repo": repo_dict,
        "units": max_unit
    }

    return JsonResponse(response_dict)


def repo_list_json(request):
    return JsonResponse({'labels': [repo.label.label for repo in Repo.objects.all()]})


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
