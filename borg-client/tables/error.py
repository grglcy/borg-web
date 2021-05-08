from datetime import datetime


class Error(object):
    def __init__(self, error: str, time: datetime):
        self.error = error.strip()
        if not self.error:
            self.error = "No error information supplied"
        self.time = time

    def get_dict(self, label):
        if not label.strip():
            raise Exception("No label supplied")
        return {
            "label": label,
            "error": self.error.strip(),
            "time": self.time.isoformat()
        }
