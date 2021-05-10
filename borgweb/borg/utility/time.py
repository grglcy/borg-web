from datetime import datetime


def time_ago(time: datetime, short=False, truncate=False):
    seconds = int((datetime.utcnow() - time).total_seconds())

    return seconds_to_string(seconds, short=short, truncate=truncate)


def seconds_to_string(seconds: int, short=False, truncate=False):
    seconds = int(seconds)
    increments = [('year', 'yr', 31557600),
                  ('week', 'wk', 604800),
                  ('day', 'day', 86400),
                  ('hour', 'hr', 3600),
                  ('minute', 'min', 60),
                  ('second', 'sec', 1)]

    if seconds == 0:
        if short:
            return f"0 {increments[-1][1]}s"
        else:
            return f"0 {increments[-1][0]}s"

    time_string = ""

    remainder = seconds
    for st, sst, s in increments:
        if remainder == 0:
            break
        if short:
            st = sst
        if remainder < s or remainder == 0:
            continue
        else:
            exact, remainder = divmod(remainder, s)
            if exact > 1:
                time_string += f"{exact} {st}s, "
            else:
                time_string += f"{exact} {st}, "
            if truncate:
                break
    return time_string.strip().strip(',')[::-1].replace(' ,', ' dna ', 1)[::-1]


def subtract_months(p_date: datetime, offset):
    years, months = divmod(offset, 12)
    new_date = p_date.replace(year=p_date.year - years)
    offset -= years * 12

    if new_date.month <= offset:
        offset -= new_date.month
        return new_date.replace(month=12 - offset, year=new_date.year - 1)
    else:
        return new_date.replace(month=new_date.month - months)
