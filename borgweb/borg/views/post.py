from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache as django_cache
from ..models import Repo, Label, Archive, Cache, Error, Location
from ..forms import RepoForm, ArchiveForm, ErrorForm, LocationForm, ToggleVisibility


@permission_required("borg.change_repo")
def toggle_visibility(request):
    if request.method == 'POST':
        form = ToggleVisibility(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data

            label = get_object_or_404(Label, label=cdata['label'])

            label.visible = not label.visible

            label.save()
            django_cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ToggleVisibility()

    return render(request, 'borg/post/toggle.html', {'form': form})


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
            django_cache.clear()

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
            django_cache.clear()

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
            django_cache.clear()

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
            django_cache.clear()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = LocationForm()

    return render(request, 'borg/post/location.html', {'form': form})