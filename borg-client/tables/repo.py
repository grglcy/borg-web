from datetime import datetime, timezone
from pathlib import Path


class Repo(object):
    def __init__(self, fingerprint: str, location, last_modified: datetime):
        self.fingerprint = fingerprint
        self.location = location
        self.last_modified = last_modified

    @classmethod
    def from_json(cls, json: dict):
        uuid = json['id']
        location = Path(json['location'])
        last_modified = datetime.fromisoformat(json['last_modified']) \
            .astimezone(tz=timezone.utc) \
            .replace(tzinfo=None)
        return cls(uuid, location, last_modified)

    def get_dict(self, label):
        if not label.strip():
            raise Exception("No label supplied")
        return {
            "label": label,
            "fingerprint": self.fingerprint,
            "location": self.location,
            "last_modified": self.last_modified.isoformat()
        }
