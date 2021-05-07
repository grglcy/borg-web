from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Repo, Label, Archive, Cache, Error
from django.urls import reverse
from .forms import RepoForm, ArchiveForm, ErrorForm


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


def get_archive(request):
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

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ArchiveForm()

    return render(request, 'borg/archive.html', {'form': form})


def get_error(request):
    if request.method == 'POST':
        form = ErrorForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            label, _ = Label.objects.get_or_create(label=cdata['label'])

            error = Error(label=label, error=cdata['error'], time=cdata['time'])
            error.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ErrorForm()

    return render(request, 'borg/error.html', {'form': form})
