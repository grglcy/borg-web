from django.http import JsonResponse
from ..models import Repo
from . import repo_daily_dict


def repo_daily_json(request):
    repo_list = Repo.objects.all()
    return JsonResponse(repo_daily_dict(repo_list, 31))
