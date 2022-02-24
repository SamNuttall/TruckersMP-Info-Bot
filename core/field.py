from interactions import EmbedField

from core import emoji, util
from core.emoji import Emoji
from core.attribute import Server, TrafficServer, Location


async def get_server_field(server: dict):
    status_emoji = Emoji.UP if server[Server.online] else Emoji.DOWN
    game_emoji = Emoji.ETS2 if server[Server.game].upper() == "ETS2" else Emoji.ATS
    status = "Online" if server[Server.online] else "Offline"
    queue = server[Server.queue] if server[Server.online] else "N/A"

    name = server[Server.short_name]
    if server[Server.event]:
        await util.trim_string(server[Server.name])

    players = f"{server[Server.players]}/{server[Server.max_players]}"
    if not server[Server.online]:
        players = "N/A"

    icons = (
        Emoji.SL_ON if server[Server.speed_limiter] else Emoji.SL_OFF,
        Emoji.CO_ON if server[Server.collisions] else Emoji.CO_OFF,
        Emoji.CA_ON if server[Server.cars_for_players] else Emoji.CA_OFF,
        Emoji.AFK_ON if server[Server.afk_enabled] else Emoji.AFK_OFF,
        Emoji.PM if server[Server.promods] else ""
    )

    return EmbedField(
        name=f"{status_emoji}{game_emoji} {name}",
        value=f"**{status}:** {players}\n**In queue:** {queue}\n{' '.join(icons)}",
        inline=True,
    )


async def get_location_field(location: dict):
    server = location[Location.server]
    name = await util.trim_string(location[Location.name], 17)
    game_emoji = Emoji.ETS2 if location[Location.game].upper() == "ETS2" else Emoji.ATS
    players = location[Location.players]
    severity = emoji.TRAFFIC_SEVERITY[location[Location.severity]]

    server_name = server[TrafficServer.short_name]
    if "event" in server[TrafficServer.url]:
        server_name = await util.trim_string(server[TrafficServer.name], 9)

    return EmbedField(
        name=name,
        value=f"{game_emoji} **{server_name}\nPlayers:** {players} {util.INVISIBLE_CHAR}\n{severity}",
        inline=True,
    )

