# Core: Utils
# Provides utilities which perform functions which aid the developer

from datetime import datetime
from time import mktime
from typing import Union

import dateutil.parser
from truckersmp.cache import get_caches

INVISIBLE_CHAR = "ㅤ"


def trim_string(string: str, max_chars: int = 8, add_dots: bool = True):
    """Trims a string to a set length and adds ... to the string"""
    if len(string) > max_chars:
        string = string[:max_chars]
        if add_dots:
            string += "..."
    return string


def strip_dict_key_value(dictionaries: list, key: str):
    """Strip the value from a dictionary using a key in a list of dictionaries"""
    values = list()
    for dictionary in dictionaries:
        values.append(dictionary[key])
    return values


def get_cache_info():
    info = str()
    caches = get_caches()
    for c in caches:
        info += f"{c.get_info()}\n"
    return info


def format_time(time_data: Union[datetime, str], time_format=None):
    """Convert a datetime or ISO formatted str to a readable string using dateutil parser. Default format is 12h time"""
    if not time_format:
        time_format = '%I:%M %p'  # XX:XXam/pm
    if type(time_data) == datetime:
        time_data = time_data.isoformat()
    return dateutil.parser.isoparse(time_data).strftime(time_format)


def to_datetime(time_data: str):
    """Convert an ISO formatted str to a datetime object"""
    return datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")


def to_discord(time_data: datetime, flag: str = "f"):
    """Convert a datetime object to a Discord timestamp string"""
    unix = int(mktime(time_data.timetuple()))
    return f"<t:{unix}:{flag}>"


def get_server_via_id(servers: list, id: int):
    """Get a TruckersMP Server via it's ID."""
    for server in servers:
        if server.id == id:
            return server
