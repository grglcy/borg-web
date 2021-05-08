from django.db import models
from . import Label
from ..utility.time import time_ago
from datetime import datetime


class Error(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='errors')
    error = models.TextField()
    time = models.DateTimeField()

    def time_ago(self):
        return f"{time_ago(self.time, False, True)} ago"

