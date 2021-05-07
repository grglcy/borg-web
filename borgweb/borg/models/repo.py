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
        return f"{bytes_to_string(cache.unique_csize)}"

    def recent_errors(self):
        days = 7
        days_ago = (datetime.utcnow() - timedelta(days=7))
        errors = self.label.errors.all().filter(time__gt=days_ago)
        if len(errors) == 1:
            return f"1 error since {days} days ago"
        else:
            return f"{len(errors)} errors since {days} days ago"

    def archive_dates(self):
        days = self.get_archive_days()

    def get_archive_days(self):
        current_day = datetime.utcnow().day
        days = []
        for day in reversed(range(1, 31)):
            try:
                cday = datetime.utcnow().replace(day=day)
            except ValueError:
                continue
            if day > current_day:
                days.append(False)
            else:
                cday_archives = self.archives.all().filter(start__date=cday)
                days.append(len(cday_archives) > 0)
        return days

    def get_archive_hours_dict(self):
        return {"id": self.id,
                "label": self.label.label,
                "hours": self.get_archive_hours()}

    def get_archive_hours(self):
        hours = []
        for hour in range(24):
            chour = datetime.utcnow() - timedelta(hours=hour)
            cday_archives = self.archives.all().filter(start__date=chour.date()).filter(start__hour=chour.hour)
            hours.append(len(cday_archives) > 0)
        hours = ''.join(['H' if hour is True else '-' for hour in hours])
        return hours
