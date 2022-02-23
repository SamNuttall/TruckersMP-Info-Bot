from interactions import EmbedField

from core import emoji, util
from core import attribute as attr
from core.emoji import Emoji
from core.attribute import Server, TrafficServer, Location


async def get_server_field(server: dict):
    status_emoji = emoji.get(Emoji.UP if server[attr.get(Server.online)] else Emoji.DOWN)
    game_emoji = emoji.get(Emoji.ETS2 if server[attr.get(Server.game)].upper() == "ETS2" else Emoji.ATS)
    status = "Online" if server[attr.get(Server.online)] else "Offline"
    queue = server[attr.get(Server.queue)] if server[attr.get(Server.online)] else "N/A"

    name = server[attr.get(Server.short_name)]
    if server[attr.get(Server.event)]:
        await util.trim_string(server[attr.get(Server.name)])

    players = f"{server[attr.get(Server.players)]}/{server[attr.get(Server.max_players)]}"
    if not server[attr.get(Server.online)]:
        players = "N/A"

    icons = (
        emoji.get(Emoji.SL_ON if server[attr.get(Server.speed_limiter)] else Emoji.SL_OFF),
        emoji.get(Emoji.CO_ON if server[attr.get(Server.collisions)] else Emoji.CO_OFF),
        emoji.get(Emoji.CA_ON if server[attr.get(Server.cars_for_players)] else Emoji.CA_OFF),
        emoji.get(Emoji.AFK_ON if server[attr.get(Server.afk_enabled)] else Emoji.AFK_OFF),
        emoji.get(Emoji.PM) if server[attr.get(Server.promods)] else ""
    )

    return EmbedField(
        name=f"{status_emoji}{game_emoji} {name}",
        value=f"**{status}:** {players}\n**In queue:** {queue}\n{' '.join(icons)}",
        inline=True,
    )


async def get_location_field(location: dict):
    server = location[attr.get(Location.server)]
    name = await util.trim_string(location[attr.get(Location.name)], 17)
    game_emoji = emoji.get(Emoji.ETS2 if location[attr.get(Location.game)].upper() == "ETS2" else Emoji.ATS)
    players = location[attr.get(Location.players)]
    severity = emoji.TRAFFIC_SEVERITY[location[attr.get(Location.severity)]]

    server_name = server[attr.get(TrafficServer.short_name)]
    if "event" in server[attr.get(TrafficServer.url)]:
        server_name = await util.trim_string(server[attr.get(TrafficServer.name)], 9)

    return EmbedField(
        name=name,
        value=f"{game_emoji} **{server_name}\nPlayers:** {players} {util.INVISIBLE_CHAR}\n{severity}",
        inline=True,
    )

