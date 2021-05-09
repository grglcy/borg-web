from math import floor, log

bytes_in_unit = 1024    # Kibibyte
units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "HiB")
# bytes_in_unit = 1000  # Kilobyte
# units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "HB")


def convert_bytes(c_bytes: int, unit: str = None) -> (float, str):
    if c_bytes == 0:
        return 0, units[0] if unit is None else unit

    if unit is None:
        index = int(floor(log(c_bytes, bytes_in_unit)))
    else:
        index = units.index(unit)

    result = round(c_bytes / pow(bytes_in_unit, index), 2)
    return result, units[index]


def bytes_to_string(c_bytes: int, unit: str = None) -> str:
    n_bytes, unit = convert_bytes(c_bytes, unit)
    return f"{n_bytes} {unit}"
