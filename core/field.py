from interactions import EmbedField

from core import emoji, util
from core.emoji import Emoji
from core.attribute import TrafficServer, Location, ServerAttributes


async def get_server_field(server: dict):
    s = ServerAttributes(server)
    return EmbedField(
        name=f"{s.status_emoji}{s.game_emoji} {s.formatted_name}",
        value=f"**{s.status}:** {s.players}\n**In queue:** {s.queue}\n{' '.join(s.icons)}",
        inline=True,
    )


async def get_location_field(location: dict):
    server = location[Location.server]
    name = util.trim_string(location[Location.name], 17)
    game_emoji = Emoji.ETS2 if location[Location.game].upper() == "ETS2" else Emoji.ATS
    players = location[Location.players]
    severity = emoji.TRAFFIC_SEVERITY[location[Location.severity]]

    server_name = server[TrafficServer.short_name]
    if "event" in server[TrafficServer.url]:
        server_name = util.trim_string(server[TrafficServer.name], 9)

    return EmbedField(
        name=name,
        value=f"{game_emoji} **{server_name}\nPlayers:** {players} {util.INVISIBLE_CHAR}\n{severity}",
        inline=True,
    )

