"""
Provides global utility functions
"""

from datetime import datetime
from time import mktime
from typing import Union

import interactions as ipy

import dateutil.parser
from truckersmp.cache import get_caches

INVISIBLE_CHAR = "ㅤ"


def trim_string(string: str, max_chars: int = 8, add_dots: bool = True) -> str:
    """Trims a string to a set length and adds ... to the string"""
    if len(string) > max_chars:
        string = string[:max_chars]
        if add_dots:
            string += "..."
    return string


def strip_dict_key_value(dictionaries: list, key: str) -> list:
    """
    Strip the value from a dictionary using a key in a list of dictionaries

    Example:
        Consider a list like this passed into dictionaries:
            [
                {
                    "key1": "dict1-val1",
                    "key2": "dict1-val2",
                },
                {
                    "key1": "dict2-val1",
                    "key2": "dict2-val2",
                }
            ]
        This function takes a key, and will create a list of values.
        If "key2" is the key, ["dict1-val2", "dict2-val2"] would be returned

    Raises a KeyError if the key is not in any of the given dictionaries
    """
    values = list()
    for dictionary in dictionaries:
        values.append(dictionary[key])
    return values


def get_cache_info() -> str:
    """Get the bot's cache info from async-truckersmp (does not get ipy library cache info)"""
    info = str()
    caches = get_caches()
    for c in caches:
        info += f"{c.get_info()}\n"
    return info


def format_time(time_data: Union[datetime, str], time_format=None) -> str:
    """Convert a datetime or ISO formatted str to a readable string using dateutil parser. Default format is 12h time"""
    if not time_format:
        time_format = '%I:%M %p'  # XX:XXam/pm
    if type(time_data) == datetime:
        time_data = time_data.isoformat()
    return dateutil.parser.isoparse(time_data).strftime(time_format)


def iso_to_datetime(time_data: str) -> datetime:
    """Convert an ISO formatted str to a datetime object"""
    return datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")


def datetime_to_discord_str(time_data: datetime, flag: str = "f") -> str:
    """
    Convert a datetime object to a Discord timestamp string
    See https://discord.com/developers/docs/reference#message-formatting-timestamp-styles for info
    """
    unix = int(mktime(time_data.timetuple()))
    return f"<t:{unix}:{flag}>"


def get_server_via_id(servers: list, id: int):
    """Get a TruckersMP Server via it's ID."""
    for server in servers:
        if server.id == id:
            return server


def get_list_from_events(events, list_type: str = "Featured"):
    """Get a specific list (eg. Featured, Now) from an Events response"""
    match list_type:
        case "featured":
            events = events.featured
        case "upcoming":
            events = events.today + events.upcoming  # Upcoming should include todays event's too
        case _:
            events = events.now
    return events


def is_component_author(ctx: ipy.ComponentContext):
    """Check if a user using a component is the author of the component's original command"""
    return ctx.author_id == ctx.message.interaction._user_id
