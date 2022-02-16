from interactions import Embed, EmbedField

from core import emoji, utils
from core.emoji import Emoji


async def get_server_field(server: dict):
    status_emoji = emoji.get(Emoji.UP if server['online'] else Emoji.DOWN)
    game_emoji = emoji.get(Emoji.ETS2 if server['game'].upper() == "ETS2" else Emoji.ATS)
    name = server['shortname'] if not server['event'] else await utils.trim_string(server['name'])
    status = "Online" if server['online'] else "Offline"
    players = f"{server['players']}/{server['maxplayers']}" if server['online'] else "N/A"
    queue = server['queue'] if server['online'] else "N/A"

    sl_emoji = emoji.get(Emoji.SL_ON if server['speedlimiter'] else Emoji.SL_OFF)
    co_emoji = emoji.get(Emoji.CO_ON if server['collisions'] else Emoji.CO_OFF)
    ca_emoji = emoji.get(Emoji.CA_ON if server['carsforplayers'] else Emoji.CA_OFF)
    afk_emoji = emoji.get(Emoji.AFK_ON if server['afkenabled'] else Emoji.AFK_OFF)
    pm_emoji = emoji.get(Emoji.PM) if server['promods'] else ""
    icons = f"{sl_emoji} {co_emoji} {ca_emoji} {afk_emoji} {pm_emoji}"

    return EmbedField(
        name=f"{status_emoji}{game_emoji} {name}",
        value=f"**{status}:** {players}\n**In queue:** {queue}\n{icons}",
        inline=True,
    )


async def get_location_field(location: dict):
    server = location['server']
    name = await utils.trim_string(location['name'], 17)
    game_emoji = emoji.get(Emoji.ETS2 if location['game'].upper() == "ETS2" else Emoji.ATS)
    server_name = server['short'] if "event" not in server['url'] else await utils.trim_string(server['name'], 9)
    players = location['players']
    severity = emoji.TRAFFIC_SEVERITY[location['severity']]

    return EmbedField(
        name=name,
        value=f"{game_emoji} **{server_name}\nPlayers:** {players} {utils.INVISIBLE_CHAR}\n{severity}",
        inline=True,
    )

