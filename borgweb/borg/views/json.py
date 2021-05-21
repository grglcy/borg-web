from datetime import datetime, timedelta
from django.http import JsonResponse
from ..models import Repo
from ..utility import data
import calendar


def repo_monthly_json(request, months_ago: int = 12):
    date_labels = monthly_date_labels(months_ago)

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


def monthly_date_labels(months_ago: int):
    dates = []
    current_date = datetime.utcnow().date()
    current_year = current_date.year
    current_month = current_date.month
    dates.append(current_date)
    for month in range(months_ago - 1):
        if current_month == 1:
            current_year -= 1
            current_month = 12
        else:
            current_month -= 1
        last_day = calendar.monthrange(current_year, current_month)[1]
        current_date = current_date.replace(year=current_year, month=current_month, day=last_day)
        dates.append(current_date)

    return [date.strftime("%b %Y") for date in dates][::-1]


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

