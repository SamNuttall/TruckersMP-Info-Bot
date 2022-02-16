from interactions import Embed, EmbedField, EmbedFooter, EmbedImageStruct
from datetime import datetime

from core import fields as embed_fields

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
            name=":cry: All locations have no players",
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
                          total_players: int = None, max_total_players: int = None,
                          total_in_queue: int = None, ingame_time: str = None):
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
    if ingame_time:
        description += f"\n**:alarm_clock: In-game time:** {ingame_time}"
    return description


async def servers_stats(servers: list, filter_by_game: str = None, ingame_time: str = None):
    """Takes a list of servers and creates an embed from them"""
    fields = []
    total_players = 0
    max_total_players = 0
    total_in_queue = 0
    for server in servers:
        if filter_by_game and filter_by_game != server['game']:
            continue
        total_players += server['players']
        max_total_players += server['maxplayers']
        total_in_queue += server['queue']
        fields.append(await embed_fields.get_server_field(server))

    fields = await format_fields(fields, 0)
    if not ingame_time:
        ingame_time = "Unknown"
    return Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        description=await get_description(filter_by_game=filter_by_game,
                                          total_players=total_players,
                                          max_total_players=max_total_players,
                                          total_in_queue=total_in_queue,
                                          ingame_time=ingame_time),
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
    for location in locations:
        add = True
        for filter_by in filter_bys:
            if filter_by and filter_by not in (location['game'], location['server']['url']):
                add = False
        if not add:
            continue
        if location['players'] == 0:
            break
        fields.append(await embed_fields.get_location_field(location))
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
