"""
Handles the creation of embed fields (often those that are used in mass and follow a similar structure)
Functions here will return an EmbedField created based on the data given.
"""

import interactions as ipy

from common import utils
from common.data.models import Server, Location
from common.utils import INVISIBLE_CHAR  # TODO: Review the location of this (invisible char)


def get_server(server):
    s = Server(server)
    return ipy.EmbedField(
        name=f"{s.status_emoji}{s.game_emoji} {s.formatted_name}",
        value=f"**{s.status}:** {s.players}\n**In queue:** {s.queue}\n{' '.join(s.icons)}",
        inline=True,
    )


def get_location(location: dict):
    lo = Location(location)
    return ipy.EmbedField(
        name=lo.trimmed_name,
        value=f"{lo.game_emoji} **{lo.trimmed_server_name}\n"
              f"Players:** {lo.players} {INVISIBLE_CHAR}\n{lo.severity_bar}",
        inline=True,
    )


def get_event(event, include_link: bool = False):
    e = event
    start_time = utils.datetime_to_discord_str(utils.iso_to_datetime(event.start_at))
    field_value = (
        f"> :round_pushpin: {e.departure.location}, {e.departure.city}\n"
        f"> :alarm_clock: {start_time}\n"
        f"> :desktop: {e.server.name} ({e.game})\n"
    )
    if include_link:
        field_value += f"*[View Online](https://truckersmp.com/events/{e.id})*"
    return ipy.EmbedField(
        name=event.name,
        value=field_value
    )
