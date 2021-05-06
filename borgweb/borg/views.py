from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Repo, Label


def index(request):
    repo_list = Repo.objects.all()
    label_list = Label.objects.all()
    # template = loader.get_template('borg/index.html')
    context = {
        'repo_list': repo_list,
        'label_list': label_list,
        }
    # return HttpResponse(template.render(context, request))
    return render(request, 'borg/index.html', context)
