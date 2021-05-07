from django.db import models


class Cache(models.Model):
    total_chunks = models.IntegerField()
    total_csize = models.IntegerField()
    total_size = models.IntegerField()
    total_unique_chunks = models.IntegerField()
    unique_csize = models.IntegerField()
    unique_size = models.IntegerField()
