from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed

from .models import Repo, Label
from django.urls import reverse
from .forms import RepoForm


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
        form = RepoForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data

            repo_query = Repo.objects.all().filter(fingerprint=cdata['fingerprint'])
            if len(repo_query) > 0:
                label = repo_query[0].label
                label.label = cdata['label']
                label.save()

            label, _ = Label.objects.get_or_create(label=cdata['label'])
            label.save()
            repo, repo_exists = Repo.objects.update_or_create(fingerprint=cdata['fingerprint'],
                                                              defaults={'location': cdata['location'],
                                                                        'last_modified': cdata['last_modified'],
                                                                        'label': label})
            repo.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = RepoForm()

    return render(request, 'borg/repo.html', {'form': form})
