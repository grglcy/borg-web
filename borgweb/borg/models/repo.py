from django.db import models
from datetime import datetime, timedelta
from ..utility.time import seconds_to_string
from ..utility.data import bytes_to_string


class Repo(models.Model):
    fingerprint = models.TextField()
    location = models.TextField()
    last_modified = models.DateTimeField()

    class Meta:
        db_table = 'repo'

    def last_backup(self):
        latest = self.latest_archive().start.replace(tzinfo=None)
        seconds_since = int((datetime.utcnow() - latest).total_seconds())
        return f"{seconds_to_string(seconds_since, False, True)} ago"

    def latest_archive(self):
        return self.archives.order_by('-start')[0]

    def size(self):
        cache = self.latest_archive().cache
        size = bytes_to_string(cache.unique_size)
        csize = bytes_to_string(cache.unique_csize)
        return f"{size}/{csize}"

    def recent_errors(self):
        days = 7
        days_ago = (datetime.utcnow() - timedelta(days=7))
        errors = self.label.errors.all().filter(time__gt=days_ago)
        if len(errors) == 1:
            return f"1 error since {days} days ago"
        else:
            return f"{len(errors)} errors since {days} days ago"
