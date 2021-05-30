from datetime import datetime
import calendar


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

        year = new_date.year - 1
        month = 12 - offset

        last_day = calendar.monthrange(year, month)[1]
        if new_date.day > last_day:
            new_date = new_date.replace(day=last_day)

        return new_date.replace(month=month, year=year)
    else:
        year = new_date.year
        month = new_date.month - months

        last_day = calendar.monthrange(year, month)[1]
        if new_date.day > last_day:
            new_date = new_date.replace(day=last_day)
        return new_date.replace(month=month)


def last_day_previous_months(months_ago: int):
    dates = []
    current_date = datetime.utcnow().date()
    current_year = current_date.year
    current_month = current_date.month
    dates.append(current_date)
    for month in range(months_ago - 1):
        if current_month == 1:
            current_year -= 1
            current_month = 12
        else:
            current_month -= 1
        last_day = calendar.monthrange(current_year, current_month)[1]
        current_date = current_date.replace(year=current_year, month=current_month, day=last_day)
        dates.append(current_date)

    return dates[::-1]
