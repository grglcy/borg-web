from math import floor, log


def bytes_to_string(bytes: int):
    suffixes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "HB")
    if bytes == 0:
        return f"0{suffixes[0]}"
    else:
        index = int(floor(log(bytes, 1024)))
        s = round(bytes / pow(1024, index), 2)
        return f"{s}{suffixes[index]}"
