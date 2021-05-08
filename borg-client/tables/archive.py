from datetime import datetime, timezone


class Archive(object):
    def __init__(self, fingerprint: str, name: str, start: datetime, end: datetime, file_count: int, original_size: int,
                 compressed_size: int, deduplicated_size: int):
        self.fingerprint = fingerprint
        self.name = name
        self.start = start
        self.end = end
        self.file_count = file_count
        self.original_size = original_size
        self.compressed_size = compressed_size
        self.deduplicated_size = deduplicated_size

    @classmethod
    def from_json(cls, json: dict):
        fingerprint = json['id']
        name = json['name']
        start = datetime.fromisoformat(json['start']).astimezone(tz=timezone.utc).replace(tzinfo=None)
        end = datetime.fromisoformat(json['end']).astimezone(tz=timezone.utc).replace(tzinfo=None)

        stats_json = json['stats']
        file_count = stats_json['nfiles']
        original_size = stats_json['original_size']
        compressed_size = stats_json['compressed_size']
        deduplicated_size = stats_json['deduplicated_size']

        return cls(fingerprint, name, start, end, file_count, original_size, compressed_size, deduplicated_size)

    def get_dict(self, label):
        if not label.strip():
            raise Exception("No label supplied")
        return {
            "label": label,
            "fingerprint": self.fingerprint,
            "name": self.name,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "file_count": self.file_count,
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "deduplicated_size": self.deduplicated_size
        }
