from truckersmp.models import Player, Event
from interactions import Embed, EmbedField, EmbedFooter, EmbedImageStruct
from datetime import datetime

from core import field as embed_fields
from core import util, format
from core.attribute import ServerAttributes


TRUCKERSMP_LOGO = "https://truckersmp.com/assets/img/avatar.png"
BOT_AVATAR_URL = "https://i.imgur.com/pX5Q4zH.png"
EMBED_COLOUR = 0x826b59
EMBED_ERROR_COLOUR = 0xFF0000


async def generic_embed(title: str, colour=None):
    if colour is None:
        colour = EMBED_ERROR_COLOUR
    return Embed(
        title=title,
        color=colour
    )


async def item_not_found(item: str):
    return Embed(
        title=f":mag: {item} not found",
        color=EMBED_ERROR_COLOUR
    )


async def item_not_found_detailed(item, desc):
    embed = await item_not_found(item)
    embed.description = desc
    return embed


async def generic_error():
    return Embed(
        title=f":neutral_face: Something went wrong...",
        color=EMBED_ERROR_COLOUR
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
            name="No Results!",
            value=f"**:cry: All locations have no players.**",
            inline=False,
        ))
    elif input_len < expected_length:
        fields.append(EmbedField(
            name="⠀",
            value=f"*:cry: Showing {input_len} locations; all others have no players.*",
            inline=False,
        ))
    return fields


async def get_description(filter_by_server: str = None, filter_by_game: str = None, filter_by_location: str = None,
                          total_players: int = None, max_total_players: int = None,
                          total_in_queue: int = None, ingame_time: str = None,
                          players_in_locations: int = None, players_in_traffic: int = None):
    """Get the description for an embed based on the filters"""
    description_start = f"\n:pencil: **Filtered by "
    description = ""
    if filter_by_server:
        description += description_start + f"server:** {filter_by_server}"
    if filter_by_game:
        description += description_start + f"game:** {filter_by_game}"
    if filter_by_location:
        description += description_start + f"location:** {filter_by_location}"

    if total_players is not None and max_total_players is not None and total_in_queue is not None:
        description += (f"\n**:busts_in_silhouette: Total Players:** " +
                        f"{total_players}/{max_total_players} ({total_in_queue} in queue)")
    if players_in_locations is not None:
        description += f"\n**:busts_in_silhouette: Players in Locations:** {players_in_locations}"
    if players_in_traffic is not None:
        description += f"\n**:truck: Players in Traffic Jams:** {players_in_traffic}"
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
        if filter_by_game and filter_by_game != server.game:
            continue
        total_players += server.players
        max_total_players += server.max_players
        total_in_queue += server.queue
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
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=BOT_AVATAR_URL
        )
    )


async def server_stats(server: dict, ingame_time: str = None):
    """Takes a specific server and creates an embed from it"""
    if not ingame_time:
        ingame_time = "Unknown"
    s = ServerAttributes(server, promods_if_disabled=":red_circle:")
    description = await get_description(
        filter_by_server=s.short_name.upper(),
        ingame_time=ingame_time
    )
    speed_limiter = "**Speed Limiter:** Enabled" if s.speed_limiter else "**Speed Limiter:** Disabled"
    collisions = "**Collisions:** Enabled" if s.collisions else "**Collisions:** Disabled"
    cars = "**Cars for Players:** Enabled" if s.cars_for_players else "**Cars for Players:** Disabled"
    afk_kick = "**AFK Kick:** Enabled" if s.afk_enabled else "**AFK Kick:** Disabled"
    promods = "**Promods:** Enabled" if s.promods else "**Promods:** Disabled"
    description += (
        "\n\n"
        f"> :desktop: **{s.name}** ({s.short_name})\n"
        f"> {s.status_emoji} **Status:** {s.status}\n"
        f"> {s.game_emoji} **Game:** {s.game}\n"
        f"> :busts_in_silhouette: **Players:** {s.players} ({s.percent_players}%)\n"
        f"> :watch: **In Queue:** {s.queue}\n"
        f"> {s.speed_limiter_icon} {speed_limiter}\n"
        f"> {s.collisions_icon} {collisions}\n"
        f"> {s.cars_for_players_icon} {cars}\n"
        f"> {s.afk_enabled_icon} {afk_kick}\n"
        f"> {s.promods_icon} {promods}"
        f"\n> :label: **Type:** {s.type}"
    )
    return Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        description=description,
        thumbnail=EmbedImageStruct(url=TRUCKERSMP_LOGO)._json,
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=BOT_AVATAR_URL
        )
    )


async def traffic_stats(locations: list, filter_by_server: str, filter_by_game: str,
                        filter_by_location: str, limit: int = 9):
    """Takes a list of traffic locations and creates an embed from them"""
    fields = []
    filter_bys = (filter_by_server, filter_by_game, filter_by_location)
    players_in_locations = 0
    players_in_traffic = 0
    for location in locations:
        add = True
        for filter_by in filter_bys:
            if filter_by and filter_by not in (location['game'], location['server']['url'], location['name']):
                add = False
        if not add:
            continue
        if location['players'] == 0:
            break
        fields.append(await embed_fields.get_location_field(location))
        players_in_locations += location['players']
        players_in_traffic += location['playersInvolvedInTrafficJams']
        if len(fields) >= limit:
            break

    fields = await format_fields(fields, limit)
    if filter_by_server:
        filter_by_server = filter_by_server.capitalize()
    if filter_by_location:
        filter_by_location = util.trim_string(filter_by_location, 20)
    return Embed(
        title=f":truck: TruckersMP | Highest Traffic Areas",
        description=await get_description(filter_by_server,
                                          filter_by_game,
                                          filter_by_location,
                                          players_in_locations=players_in_locations,
                                          players_in_traffic=players_in_traffic),
        thumbnail=EmbedImageStruct(url=TRUCKERSMP_LOGO)._json,
        url="https://traffic.krashnz.com/",
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by TruckyApp",
            icon_url=BOT_AVATAR_URL
        )
    )


async def location_stats(locations: list, filter_by: str):
    matched_locations = []
    for location in locations:
        if location.name == filter_by:
            matched_locations.append(location)

    description = await get_description()


async def player_stats(player: Player):
    """Takes a specific player and creates an embed from them"""
    p = player
    joined = await format.to_discord(await format.to_datetime(p.join_date))
    steam = f"[{p.steam_id_64}](https://steamcommunity.com/profiles/{p.steam_id_64})"
    description = (
        f"> :pencil: **Name:** {p.name}\n"
        f"> :id: **ID:** {p.id}\n"
        f"> :door: **Joined:** {joined}\n"
        f"> :video_game: **Steam ID:** {steam}\n"
        f"> :blue_circle: **Discord ID:** {p.discord_id}\n"
    )
    if p.vtc.name != "":
        vtc = f"[{p.vtc.name}](https://truckersmp.com/vtc/{p.vtc.id})"
        description += f"> :truck: **VTC:** {vtc}\n"
    if p.banned:
        banned = await format.to_discord(await format.to_datetime(p.banned_until), "R")
        description += f"> :hammer: **Unbanned:** {banned}\n"
    if p.permissions.is_game_admin:
        description += f"> :red_circle: **Player is an in-game admin!**\n"
        description += f"> :black_circle: **Role:** {p.group_name}\n"
    return Embed(
        title=f":bust_in_silhouette: TruckersMP | Player Information",
        url=f"https://truckersmp.com/user/{p.id}",
        description=description,
        thumbnail=EmbedImageStruct(url=p.avatar)._json,
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=BOT_AVATAR_URL
        )
    )


async def events_stats(events: list, list_name: str = "Events", max_size: int = 5):
    fields = []
    for index, event in enumerate(events, 1):
        fields.append(await embed_fields.get_event_field(event))
        if index == max_size:
            break

    return Embed(
        title=f":truck: TruckersMP | {list_name}",
        url="https://truckersmp.com/events",
        thumbnail=EmbedImageStruct(url=TRUCKERSMP_LOGO)._json,
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        fields=fields,
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=BOT_AVATAR_URL
        )
    )


async def event_stats(event: Event, avatar: str):
    """Takes a specific event and creates an embed from them"""
    e = event
    start_time = await format.to_discord(await format.to_datetime(e.start_at))
    if type(e.dlcs) is not dict:
        dlc_list_str = "None"
    else:
        dlc_list = list(e.dlcs.values())
        dlc_list_str = dlc_list[0]
        if len(dlc_list) > 1:
            dlc_list_str += f" *(+{len(dlc_list) - 1} others)*"

    description = (
        f"__Information__\n"
        f":round_pushpin: **Location:** {e.departure.location}, {e.departure.city}\n"
        f":house: **Destination:** {e.arrive.location}, {e.arrive.city}\n"
        f":alarm_clock: **Time:** {start_time}\n"
        f":desktop: **Server:** {e.server.name}\n"
        f":video_game: **Game:** {e.game}\n"
        f"\n"
        f"__Details__\n"
        f":map: **DLCs Required:** {dlc_list_str}\n"
        f":busts_in_silhouette: **Attendances:** {e.attendances.confirmed} *({e.attendances.unsure} unsure)*\n"
        f":bust_in_silhouette: **Creator:** [{e.user.username}](https://truckersmp.com/user/{e.user.id})"
    )

    return Embed(
        title=f"{e.name}",
        url=f"https://truckersmp.com/events/{e.id}",
        image=EmbedImageStruct(url=e.map),
        thumbnail=EmbedImageStruct(url=avatar)._json,
        description=description,
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        footer=EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=BOT_AVATAR_URL
        )
    )


async def bot_info(avatar_url, invite_link, privacy_policy, source_code):
    fields = [
        EmbedField(
            name="About",
            value=f"Hi, I'm Alfie! :wave:\nA small companion for TruckersMP stats.\nThanks for using me :)"
        ),
        EmbedField(
            name="Commands",
            value=f"I fully support slash commands!\nType **/** in chat for more"
        ),
        EmbedField(
            name="Useful Links",
            value=f":robot: [Invite]({invite_link}) | "
                  f":shield: [Privacy Policy]({privacy_policy}) | "
                  f":mag: [Source Code]({source_code})"
        )
    ]
    return Embed(
        title=":page_facing_up: Bot Information",
        fields=fields,
        color=EMBED_COLOUR,
        timestamp=str(datetime.utcnow()),
        footer=EmbedFooter(
            text="Developed with love by Sam#9210",
            icon_url=BOT_AVATAR_URL
        )
    )
