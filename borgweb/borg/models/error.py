from django.db import models
from . import Label


class Error(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='errors')
    error = models.TextField()
    time = models.DateTimeField()
