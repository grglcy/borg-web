from django.db import models
from . import Repo, Cache


class Archive(models.Model):
    fingerprint = models.TextField(unique=True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_count = models.BigIntegerField()
    original_size = models.BigIntegerField()
    compressed_size = models.BigIntegerField()
    deduplicated_size = models.BigIntegerField()
    cache = models.OneToOneField(Cache, on_delete=models.CASCADE)

