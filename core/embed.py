import core.emoji
from interactions import Embed, EmbedField, EmbedFooter
from datetime import datetime

from core import emoji
from core.emoji import Emoji


async def item_not_found(item: str):
    return Embed(
        title=f":mag: {item} not found",
        color=0xFF0000
    )


async def generic_error():
    return Embed(
        title=f":neutral_face: Something went wrong...",
        color=0xFF0000
    )


async def trim_name(name: str, max_chars: int = 10, add_dots: bool = True):
    """Trims a string (server name) to a set length and adds ... to the string"""
    if len(name) > max_chars:
        name = name[:max_chars]
        if add_dots:
            name += "..."
    return name


async def servers_stats(servers: list, filter_by_game: str = None):
    """Takes a list of servers and creates an embed from them"""
    fields = []
    for server in servers:
        if filter_by_game and filter_by_game != server['game']:
            continue
        status_emoji = emoji.get(Emoji.UP if server['online'] else Emoji.DOWN)
        game_emoji = emoji.get(Emoji.ETS2 if server['game'].upper() == "ETS2" else Emoji.ATS)
        name = server['shortname'] if not server['event'] else await trim_name(server['name'])
        status = "Online" if server['online'] else "Offline"
        players = f"{server['players']}/{server['maxplayers']}" if server['online'] else "N/A"
        queue = server['queue'] if server['online'] else "N/A"

        sl_emoji = emoji.get(Emoji.SL_ON if server['speedlimiter'] else Emoji.SL_OFF)
        co_emoji = emoji.get(Emoji.CO_ON if server['collisions'] else Emoji.CO_OFF)
        ca_emoji = emoji.get(Emoji.CA_ON if server['carsforplayers'] else Emoji.CA_OFF)
        afk_emoji = emoji.get(Emoji.AFK_ON if server['afkenabled'] else Emoji.AFK_OFF)
        pm_emoji = emoji.get(Emoji.PM) if server['promods'] else ""
        icons = f"{sl_emoji} {co_emoji} {ca_emoji} {afk_emoji} {pm_emoji}"

        invisible_char = "ㅤ"

        fields.append(EmbedField(
            name=f"{status_emoji}{game_emoji} {name}",
            value=f"**{status}:** {players} {invisible_char}\n**In queue:** {queue}\n{icons}",
            inline=True,
        ))
    return Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        color=0x017af4,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
        )
    )


async def server_stats(server: dict):
    """"""
