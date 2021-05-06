from django.db import models


class Repo(models.Model):
    fingerprint = models.TextField()
    location = models.TextField()
    last_modified = models.DateTimeField()

    class Meta:
        db_table = 'repo'


class Archive(models.Model):
    fingerprint = models.TextField()
    repo_id = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_count = models.IntegerField()
    original_size = models.IntegerField()
    compressed_size = models.IntegerField()
    deduplicated_size = models.IntegerField()

    class Meta:
        db_table = 'archive'


class Cache(models.Model):
    archive_id = models.ForeignKey(Archive, on_delete=models.CASCADE)
    total_chunks = models.IntegerField()
    total_csize = models.IntegerField()
    total_size = models.IntegerField()
    total_unique_chunks = models.IntegerField()
    unique_csize = models.IntegerField()
    unique_size = models.IntegerField()

    class Meta:
        db_table = 'cache'


class Label(models.Model):
    repo_id = models.ForeignKey(Repo, on_delete=models.CASCADE)
    label = models.TextField()

    class Meta:
        db_table = 'label'


class Error(models.Model):
    label_id = models.ForeignKey(Label, on_delete=models.CASCADE)
    error = models.TextField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'error'
