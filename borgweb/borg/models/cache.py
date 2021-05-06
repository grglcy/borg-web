from django.db import models
from . import Archive


class Cache(models.Model):
    archive = models.OneToOneField(Archive, on_delete=models.CASCADE)
    total_chunks = models.IntegerField()
    total_csize = models.IntegerField()
    total_size = models.IntegerField()
    total_unique_chunks = models.IntegerField()
    unique_csize = models.IntegerField()
    unique_size = models.IntegerField()

    class Meta:
        db_table = 'cache'