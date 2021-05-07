from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Repo
from .forms import RepoForm
from django.urls import reverse


def index(request):
    repo_list = Repo.objects.all()

    hour_list = [repo.get_archive_hours_dict() for repo in repo_list]
    context = {
        'repo_list': repo_list,
        'hour_list': hour_list
        }
    return render(request, 'borg/index.html', context)


def get_repo(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RepoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = RepoForm()

    return render(request, 'borg/repo.html', {'form': form})
