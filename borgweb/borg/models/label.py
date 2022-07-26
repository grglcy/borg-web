from django.db import models


class Label(models.Model):
    label = models.TextField(blank=True, unique=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.label
