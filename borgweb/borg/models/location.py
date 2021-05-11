from django.db import models
from pathlib import Path
from datetime import datetime

ACCESS_DENIED = -2
INVALID_PATH = -1
NON_EXISTENT = 0
FILE = 1
DIRECTORY = 2
SYMLINK = 3
MOUNT_POINT = 4

DESCRIPTION = {
    INVALID_PATH: "path",
    NON_EXISTENT: "path",
    FILE: "file",
    DIRECTORY: "directory",
    SYMLINK: "symbolic link",
    MOUNT_POINT: "mount point",
    ACCESS_DENIED: "access denied",
}


class Location(models.Model):
    label = models.TextField(unique=True)
    path = models.TextField()
    last_checked = models.DateTimeField(null=True)

    def __path_type(self):
        try:
            path = Path(self.path)
            path.exists()
        except OSError:
            return INVALID_PATH
        except ValueError:
            return INVALID_PATH
        try:
            if not path.exists():
                return NON_EXISTENT
            elif path.is_symlink():
                return SYMLINK
            elif path.is_mount():
                return MOUNT_POINT
            elif path.is_dir():
                return DIRECTORY
            elif path.is_file():
                return FILE
        except PermissionError:
            return ACCESS_DENIED

    def exists(self):
        path_type = self.__path_type()

        if self.invalid():
            return False
        elif path_type in [FILE, DIRECTORY, SYMLINK, MOUNT_POINT]:
            self.last_checked = datetime.utcnow()
            return True

    def type_description(self):
        return DESCRIPTION[self.__path_type()]

    def invalid(self):
        return self.__path_type() in [INVALID_PATH, NON_EXISTENT, ACCESS_DENIED]

    def have_permission(self):
        return self.__path_type() != ACCESS_DENIED

    def short_description(self):
        type = self.__path_type()
        type_description = self.type_description()
        existence = "exists" if self.exists() else "does not exist"

        if self.exists():
            return f"{type_description} {self.path} {existence}"
