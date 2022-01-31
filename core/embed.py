from interactions import Embed, EmbedField, EmbedFooter, EmbedImageStruct
from datetime import datetime

from core import emoji
from core.emoji import Emoji

TRUCKERSMP_LOGO = "https://truckersmp.com/assets/img/avatar.png"


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


async def trim_name(name: str, max_chars: int = 8, add_dots: bool = True):
    """Trims a string (server name) to a set length and adds ... to the string"""
    if len(name) > max_chars:
        name = name[:max_chars]
        if add_dots:
            name += "..."
    return name


async def format_fields(fields: list, expected_length: int = 9):
    """Add extra fields to display extra info and align content"""
    input_len = len(fields)
    if len(fields) % 3 == 2:
        fields.append(EmbedField(
            name=f"⠀",
            value=f"⠀",
            inline=True
        ))
    if input_len == 0:
        fields.append(EmbedField(
            name=":mag: :cry: All locations have no players",
            value=f"I've searched all over this server but it looks like all locations have no players.",
            inline=False,
        ))
    elif input_len < expected_length:
        fields.append(EmbedField(
            name="Other locations have no players",
            value=f"All other locations have no traffic",
            inline=False,
        ))
    return fields


async def get_description(filter_by_server: str = None, filter_by_game: str = None,
                          total_players: int = None, max_total_players: int = None, total_in_queue: int = None):
    """Get the description for an embed based on the filters"""
    description = f":pencil: **Filtered by "
    if filter_by_server:
        description += f"server:** {filter_by_server.capitalize()}"
    elif filter_by_game:
        description += f"game:** {filter_by_game}"
    else:
        description = ""
    if total_players is not None and max_total_players is not None and total_in_queue is not None:
        description += (f"\n**:busts_in_silhouette: Total Players:** " +
                        f"{total_players}/{max_total_players} ({total_in_queue} in queue)")
    return description


async def servers_stats(servers: list, filter_by_game: str = None):
    """Takes a list of servers and creates an embed from them"""
    fields = []
    total_players = 0
    max_total_players = 0
    total_in_queue = 0
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
        total_players += server['players']
        max_total_players += server['maxplayers']
        total_in_queue += server['queue']

        fields.append(EmbedField(
            name=f"{status_emoji}{game_emoji} {name}",
            value=f"**{status}:** {players}\n**In queue:** {queue}\n{icons}",
            inline=True,
        ))
    fields = await format_fields(fields, 0)
    return Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        description=await get_description(filter_by_game=filter_by_game,
                                          total_players=total_players,
                                          max_total_players=max_total_players,
                                          total_in_queue=total_in_queue),
        thumbnail=EmbedImageStruct(url=TRUCKERSMP_LOGO)._json,
        color=0x017af4,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
        )
    )


async def server_stats(server: dict):
    """"""


async def traffic_stats(locations: list, filter_by_server: str, filter_by_game: str, limit: int = 9):
    """Takes a list of traffic locations and creates an embed from them"""
    fields = []
    filter_bys = (filter_by_server, filter_by_game)
    severity_emoji = (
        emoji.get(Emoji.T_DEF),
        emoji.get(Emoji.T_LOW),
        emoji.get(Emoji.T_MOD),
        emoji.get(Emoji.T_CON),
        emoji.get(Emoji.T_HEV)
    )
    se = severity_emoji
    severity_icons = {
        'Empty': f"{se[0]} " * 4,
        'Fluid': f"{se[1]} " + f"{se[0]}" * 3,
        'Moderate': f"{se[1]} {se[2]} " + f"{se[0]}" * 2,
        'Congested': f"{se[1]} {se[2]} {se[3]} {se[0]}",
        'Heavy': f"{se[1]} {se[2]} {se[3]} {se[4]}"
    }
    for location in locations:
        add = True
        for filter_by in filter_bys:
            if filter_by and filter_by not in (location['game'], location['server']['url']):
                add = False
        if not add:
            continue

        server = location['server']

        name = await trim_name(location['name'], 17)
        game_emoji = emoji.get(Emoji.ETS2 if location['game'].upper() == "ETS2" else Emoji.ATS)
        server_name = server['short'] if "event" not in server['url'] else await trim_name(server['name'], 9)
        players = location['players']
        severity = severity_icons[location['severity']]

        invisible_char = "ㅤ"

        if players == 0:
            break

        fields.append(EmbedField(
            name=name,
            value=f"{game_emoji} **{server_name}\nPlayers:** {players} {invisible_char}\n{severity}",
            inline=True,
        ))
        if len(fields) >= limit:
            break
    fields = await format_fields(fields, limit)
    return Embed(
        title=f":truck: TruckersMP | Highest Traffic Areas",
        description=await get_description(filter_by_server, filter_by_game),
        thumbnail=EmbedImageStruct(url=TRUCKERSMP_LOGO)._json,
        url="https://traffic.krashnz.com/",
        color=0x017af4,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by Krashnz via TruckyApp",
        )
    )
