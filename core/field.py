from interactions import EmbedField

from core.util import INVISIBLE_CHAR
from core.attribute import ServerAttributes, LocationAttributes


async def get_server_field(server):
    s = ServerAttributes(server)
    return EmbedField(
        name=f"{s.status_emoji}{s.game_emoji} {s.formatted_name}",
        value=f"**{s.status}:** {s.players}\n**In queue:** {s.queue}\n{' '.join(s.icons)}",
        inline=True,
    )


async def get_location_field(location: dict):
    lo = LocationAttributes(location)
    return EmbedField(
        name=lo.trimmed_name,
        value=f"{lo.game_emoji} **{lo.server_name}\nPlayers:** {lo.players} {INVISIBLE_CHAR}\n{lo.severity_bar}",
        inline=True,
    )
