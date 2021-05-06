from django.db import models
from . import Repo


class Archive(models.Model):
    fingerprint = models.TextField()
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name='archives')
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_count = models.IntegerField()
    original_size = models.IntegerField()
    compressed_size = models.IntegerField()
    deduplicated_size = models.IntegerField()

    class Meta:
        db_table = 'archive'
