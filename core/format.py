import dateutil.parser
from datetime import datetime
from typing import Union


async def format_time(time_data: Union[datetime, str], time_format=None):
    """Convert a datetime or ISO formatted str to a readable string using dateutil parser. Default format is 12h time"""
    if not time_format:
        time_format = '%I:%M %p'  # XX:XXam/pm
    if type(time_data) == datetime:
        time_data = time_data.isoformat()
    return dateutil.parser.isoparse(time_data).strftime(time_format)
