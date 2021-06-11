import re
from datetime import datetime

from dateutil import tz


def check_numeric(data_type, value):
    """Parse the given value to the given numeric data type (int or float)"""
    try:
        result = data_type(value)
    except (ValueError, TypeError):
        return None
    return result


def get_string(value):
    """Get a string value after stripping it of leading/trailing whitespaces"""
    return str(value).strip() if value else None


def transform_string_from_camelcase(value):
    """Transform a string from camelcase to lowercase with underscores"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).replace('__', '_').lower()


def get_datetime(value, date_format, is_datetime=True):
    """Parse the given value to a date or datetime object according to the given format"""
    if not value:
        return None
    try:
        datetime_obj = datetime.strptime(value, date_format)
        return datetime_obj if is_datetime else datetime_obj.date()
    except ValueError:
        return None


def add_local_timezone(datetime_obj, timezone):
    """Add the local time offset to a given datetime object"""
    if not datetime_obj:
        return None
    local_time = datetime_obj.replace(tzinfo=tz.gettz(timezone))
    return local_time.strftime('%Y-%m-%d %H:%M:%S%z')


def transform_to_utc(datetime_obj, timezone):
    """Transform a datetime object from local time to UTC"""
    if not datetime_obj:
        return None
    from_zone = tz.gettz(timezone)
    to_zone = tz.gettz('UTC')
    local_time = datetime_obj.replace(tzinfo=from_zone)
    return local_time.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')


def transform_from_utc(datetime_obj, timezone):
    """Transform a datetime object from UTC to local time"""
    if not datetime_obj:
        return None
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(timezone)
    local_time = datetime_obj.replace(tzinfo=from_zone)
    return local_time.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
