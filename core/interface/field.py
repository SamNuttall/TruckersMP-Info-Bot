# Core; Interface: Fields
# Handles the creation of embed fields.
# Functions here will return an EmbedField created based on the data given.

from interactions import EmbedField

import core.util
from core.models import Server, Location
from core.util import INVISIBLE_CHAR


def get_server(server):
    s = Server(server)
    return EmbedField(
        name=f"{s.status_emoji}{s.game_emoji} {s.formatted_name}",
        value=f"**{s.status}:** {s.players}\n**In queue:** {s.queue}\n{' '.join(s.icons)}",
        inline=True,
    )


def get_location(location: dict):
    lo = Location(location)
    return EmbedField(
        name=lo.trimmed_name,
        value=f"{lo.game_emoji} **{lo.trimmed_server_name}\n"
              f"Players:** {lo.players} {INVISIBLE_CHAR}\n{lo.severity_bar}",
        inline=True,
    )


def get_event(event):
    e = event
    start_time = core.util.to_discord(core.util.to_datetime(event.start_at))
    return EmbedField(
        name=event.name,
        value=(
            f":round_pushpin: {e.departure.location}, {e.departure.city}\n"
            f":alarm_clock: {start_time}\n"
            f":desktop: {e.server.name} ({e.game})\n"
        )
    )
