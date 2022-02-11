"""Parsing of date strings"""

from datetime import datetime, timedelta


def parse_date(date_str: str, end: bool = False) -> datetime:
    """Parse relative and absolute date strings of formats taken by
    `parse_relative_date` and `parse_absolute_date`"""

    if date_str[-1] in ("h", "d", "m", "y"):
        date = parse_relative_date(date_str, end)
    else:
        date = parse_absolute_date(date_str, end)
    return date.astimezone()


def parse_relative_date(date_str: str, end: bool = False) -> datetime:
    """Parse date string of relative format '3h' meaning top of the hour - 3 hours ago
    Suffix units:
    - 'h': hours
    - 'd': days
    - 'm': months
    - 'y': years
    If `end` is false a datetime at the beginning of the unit is  returned,
    if `end` is true a datetime at the end of the unit is returned.

    """
    if date_str[-1] == "h":
        date = datetime.now() - timedelta(hours=int(date_str[:-1]))
        return end_of_hour(date) if end else start_of_hour(date)

    if date_str[-1] == "d":
        date = datetime.now() - timedelta(days=float(date_str[:-1]))
        return end_of_day(date) if end else start_of_day(date)

    if date_str[-1] == "m":
        date = subtract_months(datetime.now(), int(date_str[:-1]))
        return end_of_month(date) if end else date

    if date_str[-1] == "y":
        date = subtract_years(datetime.now(), int(date_str[:-1]))
        return end_of_year(date) if end else date

    raise ValueError(f"Could not parse relative date_str '{date_str}'")


def parse_absolute_date(date_str: str, end: bool = False) -> datetime:
    """Parse date string with specified year, year+month or year+month+day

    Returns datetime object at start or end of specified date"""
    try:
        date = datetime.strptime(date_str, "%Y")
        if end:
            date = end_of_year(date)
        return date
    except ValueError:
        pass
    try:
        date = datetime.strptime(date_str, "%Y-%m")
        if end:
            date = end_of_month(date)
        return date
    except ValueError:
        pass
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if end:
            date = end_of_day(date)
        return date
    except ValueError:
        pass

    raise ValueError(f"Couldn't parse date string '{date_str}'")


def start_of_year(date: datetime) -> datetime:
    """Get datetime at start of year"""
    return datetime(year=date.year, month=1, day=1, tzinfo=date.tzinfo)


def end_of_year(date: datetime) -> datetime:
    """Get datetime at end of year"""
    return datetime(year=date.year + 1, month=1, day=1, tzinfo=date.tzinfo) - timedelta(
        microseconds=1
    )


def subtract_years(date: datetime, years: int) -> datetime:
    """Get start of year n years ago"""
    return datetime(year=date.year - years, month=1, day=1, tzinfo=date.tzinfo)


def start_of_month(date: datetime) -> datetime:
    """Get datetime at start month"""
    return datetime(year=date.year, month=date.month, day=1, tzinfo=date.tzinfo)


def end_of_month(date: datetime) -> datetime:
    """Get datetime at end of month"""
    year_delta, curr_month = divmod(date.month, 12)
    return datetime(
        year=date.year + year_delta, month=curr_month + 1, day=1, tzinfo=date.tzinfo
    ) - timedelta(microseconds=1)


def subtract_months(date: datetime, months: int) -> datetime:
    """Get datetime at start of month n months ago"""
    year_delta, new_month = divmod(date.month - months, 12)
    return datetime(
        year=date.year + year_delta - 1 * (new_month == 0),
        month=(new_month - 1) % 12 + 1,
        day=1,
        tzinfo=date.tzinfo,
    )


def start_of_day(date: datetime) -> datetime:
    """Get datetime at start of day"""
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(date: datetime) -> datetime:
    """Get datetime at end of day"""
    return start_of_day(date) + timedelta(days=1, microseconds=-1)


def start_of_hour(date: datetime) -> datetime:
    """Get datetime at start of hour"""
    return date.replace(minute=0, second=0, microsecond=0)


def end_of_hour(date: datetime) -> datetime:
    """Get datetime at end of hour"""
    return start_of_hour(date) + timedelta(hours=1, microseconds=-1)
