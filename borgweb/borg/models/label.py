from django.db import models
from . import Repo


class Label(models.Model):
    repo = models.OneToOneField(Repo, on_delete=models.CASCADE)
    label = models.TextField()

    class Meta:
        db_table = 'label'

    def __str__(self):
        return self.label