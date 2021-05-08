from datetime import datetime, timezone
from pathlib import Path


class Cache(object):
    def __init__(self, total_chunks: int, total_csize: int, total_size: int, total_unique_chunks: int,
                 unique_csize: int, unique_size: int):
        self.total_chunks = total_chunks
        self.total_csize = total_csize
        self.total_size = total_size
        self.total_unique_chunks = total_unique_chunks
        self.unique_csize = unique_csize
        self.unique_size = unique_size

    @classmethod
    def from_json(cls, json: dict):
        total_chunks = json['total_chunks']
        total_csize = json['total_csize']
        total_size = json['total_size']
        total_unique_chunks = json['total_unique_chunks']
        unique_csize = json['unique_csize']
        unique_size = json['unique_size']
        return cls(total_chunks, total_csize, total_size, total_unique_chunks, unique_csize, unique_size)

    def get_dict(self, label):
        if not label.strip():
            raise Exception("No label supplied")
        return {
            "label": label,
            "total_chunks": self.total_chunks,
            "total_csize": self.total_csize,
            "total_size": self.total_size,
            "total_unique_chunks": self.total_unique_chunks,
            "unique_csize": self.unique_csize,
            "unique_size": self.unique_size
        }
