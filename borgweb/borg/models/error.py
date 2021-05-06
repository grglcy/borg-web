from django.db import models
from . import Label


class Error(models.Model):
    label_id = models.ForeignKey(Label, on_delete=models.CASCADE)
    error = models.TextField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'error'