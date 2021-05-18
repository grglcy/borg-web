from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.urls import reverse
from .models import Repo, Label, Archive, Cache, Error, Location
from .forms import RepoForm, ArchiveForm, ErrorForm, LocationForm
from django.contrib.auth.decorators import permission_required
from .utility import data
from datetime import datetime, timedelta
from django.core.cache import cache


def index(request):
    repo_list = Repo.objects.all()
    location_list = Location.objects.all()

    # repo_dict = repo_daily_dict(repo_list, 24)

    context = {
        'repo_list': repo_list,
        # 'hour_list': repo_dict,
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


@permission_required("borg.add_repo")
def post_repo(request):
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
            cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = RepoForm()

    return render(request, 'borg/post/repo.html', {'form': form})


@permission_required("borg.add_archive")
def post_archive(request):
    if request.method == 'POST':
        form = ArchiveForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data

            repo = get_object_or_404(Repo, label__label=cdata['label'])

            cache_dict = {k: cdata[k] for k in ('total_chunks', 'total_csize', 'total_size',
                                                'total_unique_chunks', 'unique_csize', 'unique_size')}

            cache = Cache(**cache_dict)
            cache.save()

            archive_dict = {k: cdata[k] for k in ('fingerprint', 'name', 'start', 'end', 'file_count',
                                                  'original_size', 'compressed_size', 'deduplicated_size')}

            archive = Archive(**archive_dict, repo=repo, cache=cache)
            archive.save()
            cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ArchiveForm()

    return render(request, 'borg/post/archive.html', {'form': form})


@permission_required("borg.add_error")
def post_error(request):
    if request.method == 'POST':
        form = ErrorForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            label, _ = Label.objects.get_or_create(label=cdata['label'])

            error = Error(label=label, error=cdata['error'], time=cdata['time'])
            error.save()
            cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ErrorForm()

    return render(request, 'borg/post/error.html', {'form': form})


@permission_required("borg.add_location")
def post_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            label, _ = Location.objects.get_or_create(label=cdata['label'],
                                                      defaults={"path": cdata["path"]})
            label.save()
            cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = LocationForm ()

    return render(request, 'borg/post/location.html', {'form': form})


def axes(request, credentials, *args, **kwargs):
    return render(request, 'error/axes.html', {})
