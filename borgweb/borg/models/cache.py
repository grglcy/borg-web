from django.db import models


class Cache(models.Model):
    total_chunks = models.BigIntegerField()
    total_csize = models.BigIntegerField()
    total_size = models.BigIntegerField()
    total_unique_chunks = models.BigIntegerField()
    unique_csize = models.BigIntegerField()
    unique_size = models.BigIntegerField()
