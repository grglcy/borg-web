from django.db import models
from datetime import datetime, timedelta
from ..utility.time import seconds_to_string, subtract_months
from ..utility.data import bytes_to_string, convert_bytes
from . import Label


class Repo(models.Model):
    fingerprint = models.TextField(unique=True)
    location = models.TextField()
    last_modified = models.DateTimeField()
    label = models.OneToOneField(Label, on_delete=models.CASCADE, unique=True)

    def warning(self):
        if self.error():
            return True
        else:
            latest_archive = self.latest_archive()
            if latest_archive.start > datetime.utcnow() - timedelta(hours=2):
                return False
            else:
                return True

    def error(self):
        latest_archive = self.latest_archive()
        if latest_archive is None or not self.archive_after_latest_error():
            return True

        if latest_archive.start > datetime.utcnow() - timedelta(hours=4):
            return False
        else:
            return True

    def archive_after_latest_error(self):
        latest_archive = self.latest_archive()
        latest_error = self.latest_error()
        if latest_archive is None:
            return False
        elif latest_error is None:
            return True
        else:
            return latest_archive.start > latest_error.time

    def last_backup(self):
        if self.archive_set.all().exists():
            latest = self.latest_archive().start.replace(tzinfo=None)
            seconds_since = int((datetime.utcnow() - latest).total_seconds())
            return f"{seconds_to_string(seconds_since, False, True)} ago"
        else:
            return "No archives stored"

    def latest_archive(self):
        archives = self.archive_set.order_by('-start')
        if len(archives) > 0:
            return archives[0]
        else:
            return None

    def latest_error(self):
        errors = self.label.errors.all().order_by('-time')
        if len(errors) > 0:
            return errors[0]
        else:
            return None

    def size(self):
        if self.archive_set.all().exists():
            cache = self.latest_archive().cache
            return cache.unique_csize
        else:
            return 0

    def size_string(self):
        size = self.size()
        return bytes_to_string(size)

    def recent_errors(self, days: int = 7):
        days_ago = (datetime.utcnow() - timedelta(days=days))
        errors = self.label.errors.all().filter(time__gt=days_ago)
        return errors

    def get_archive_days(self, count: int = 31):
        current_day = datetime.utcnow().day
        days = []
        for day in reversed(range(1, count)):
            try:
                cday = datetime.utcnow().replace(day=day)
            except ValueError:
                continue
            if day > current_day:
                days.append(False)
            else:
                cday_archives = self.archive_set.all().filter(start__date=cday)
                days.append(len(cday_archives) > 0)
        return days

    def size_on_dates(self, units, dates: list):
        archives = self.archives_on_dates(dates)
        return self.series_csize(archives, units)

    def size_on_months(self, units, months: int = 12):
        archives = self.monthly_archives(months)
        return self.series_csize(archives, units)

    @staticmethod
    def series_times(archives):
        return [archive.start if archive is not None else None for archive in archives]

    @staticmethod
    def series_csize(archives, units=None):
        return [convert_bytes(archive.cache.unique_csize, units)[0]
                if archive is not None else None for archive in archives]

    def hourly_archive_string(self):
        return ''.join(['H' if archive is not None else '-' for archive in self.hourly_archives(8)])

    def monthly_archives(self, n_months: int = 12):
        archives = []
        for month in range(n_months):
            current_date = subtract_months(datetime.utcnow(), month)
            archive_current_month = self.archive_set.all() \
                .filter(start__year=current_date.year,
                        start__month=current_date.month) \
                .order_by('-start')
            if len(archive_current_month) > 0:
                archives.append(archive_current_month[0])
            else:
                archives.append(None)
        return archives[::-1]

    def archives_on_dates(self, dates: list):
        archives = []
        archive_queryset = self.archive_set.all()
        for date in dates:
            date_archives = archive_queryset.filter(start__date=date).order_by('-start')
            if date_archives.exists():
                archives.append(date_archives[0])
            else:
                archives.append(None)
        return archives

    def hourly_archives(self, n_hours: int = 8):
        archives = []
        for hour in range(n_hours):
            current_hour = datetime.utcnow() - timedelta(hours=hour)
            archives_hour = self.archive_set.all()\
                .filter(start__date=current_hour.date())\
                .filter(start__hour=current_hour.hour)\
                .order_by('-start')
            if len(archives_hour) > 0:
                archives.append(archives_hour[0])
            else:
                archives.append(None)
        return archives
