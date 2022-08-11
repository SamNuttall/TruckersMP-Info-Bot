import dateutil.parser
from datetime import datetime
from typing import Union
from time import mktime


async def format_time(time_data: Union[datetime, str], time_format=None):
    """Convert a datetime or ISO formatted str to a readable string using dateutil parser. Default format is 12h time"""
    if not time_format:
        time_format = '%I:%M %p'  # XX:XXam/pm
    if type(time_data) == datetime:
        time_data = time_data.isoformat()
    return dateutil.parser.isoparse(time_data).strftime(time_format)


async def to_datetime(time_data: str):
    """Convert an ISO formatted str to a datetime object"""
    return datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")


async def to_discord(time_data: datetime, flag: str = "f"):
    """Convert a datetime object to a Discord timestamp string"""
    unix = int(mktime(time_data.timetuple()))
    return f"<t:{unix}:{flag}>"
