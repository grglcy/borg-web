from django.db import models
from . import Repo, Cache


class Archive(models.Model):
    fingerprint = models.TextField(unique=True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_count = models.IntegerField()
    original_size = models.IntegerField()
    compressed_size = models.IntegerField()
    deduplicated_size = models.IntegerField()
    cache = models.OneToOneField(Cache, on_delete=models.CASCADE)

