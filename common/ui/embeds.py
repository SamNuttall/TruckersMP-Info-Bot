"""
Creates embeds ready to be sent in Discord
Does not gather data - expects it to be passed
"""

import interactions as ipy
from truckersmp.models import Player, Event
from truckersmp.cache import get_caches

import config
from common import utils
from common.ui import field as embed_fields
from common.data.models import Server


def generic_embed(title: str, colour=None):
    if colour is None:
        colour = config.EMBED_ERROR_COLOUR
    return ipy.Embed(
        title=title,
        color=colour
    )


def item_not_found(item: str):
    return ipy.Embed(
        title=f":mag: {item} not found",
        color=config.EMBED_ERROR_COLOUR
    )


def item_not_found_detailed(item, desc):
    embed = item_not_found(item)
    embed.description = desc
    return embed


def generic_error():
    return ipy.Embed(
        title=f":neutral_face: Something went wrong...",
        color=config.EMBED_ERROR_COLOUR
    )

def unhandled_error():
    return ipy.Embed(
        title=f":cry: An unexpected error occurred!",
        description="> *This has been logged and the bot owner has been notified.*",
        color=config.EMBED_ERROR_COLOUR
    )


def format_fields(fields: list, expected_length: int = 9):
    """Add extra fields to display extra info and align content"""
    input_len = len(fields)
    if len(fields) % 3 == 2:
        fields.append(ipy.EmbedField(
            name=f"⠀",
            value=f"⠀",
            inline=True
        ))
    if input_len == 0:
        fields.append(ipy.EmbedField(
            name="No Results!",
            value=f"**:cry: All locations have no players.**",
            inline=False,
        ))
    elif input_len < expected_length:
        fields.append(ipy.EmbedField(
            name="⠀",
            value=f"*:cry: Showing {input_len} locations; all others have no players.*",
            inline=False,
        ))
    return fields


def get_description(filter_by_server: str = None, filter_by_game: str = None, filter_by_location: str = None,
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


def servers_stats(servers: list, filter_by_game: str = None, ingame_time: str = None):
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
        fields.append(embed_fields.get_server(server))

    fields = format_fields(fields, 0)
    if not ingame_time:
        ingame_time = "Unknown"
    return ipy.Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        description=get_description(filter_by_game=filter_by_game,
                                    total_players=total_players,
                                    max_total_players=max_total_players,
                                    total_in_queue=total_in_queue,
                                    ingame_time=ingame_time),
        thumbnail=ipy.EmbedAttachment(url=config.TRUCKERSMP_LOGO),
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        fields=fields,
        footer=ipy.EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def server_stats(server: dict, ingame_time: str = None):
    """Takes a specific server and creates an embed from it"""
    if not ingame_time:
        ingame_time = "Unknown"
    s = Server(server, promods_if_disabled=":red_circle:")
    description = get_description(
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
    return ipy.Embed(
        title=f":truck: TruckersMP | Server Stats",
        url="https://truckersmp.com/status",
        description=description,
        thumbnail=ipy.EmbedAttachment(url=config.TRUCKERSMP_LOGO),
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        footer=ipy.EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def traffic_stats(locations: list, filter_by_server_data: list[str], filter_by_game: str,
                  filter_by_location: str, limit: int = 9):
    """Takes a list of traffic locations and creates an embed from them"""
    fields = []
    filter_by_server, server_name = filter_by_server_data  # expects: backend server url, frontend server name
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
        fields.append(embed_fields.get_location(location))
        players_in_locations += location['players']
        players_in_traffic += location['playersInvolvedInTrafficJams']
        if len(fields) >= limit:
            break

    fields = format_fields(fields, limit)
    if filter_by_server:
        filter_by_server = filter_by_server.capitalize()
    if filter_by_location:
        filter_by_location = utils.trim_string(filter_by_location, 20)
    return ipy.Embed(
        title=f":truck: TruckersMP | Highest Traffic Areas",
        description=get_description(server_name,
                                    filter_by_game,
                                    filter_by_location,
                                    players_in_locations=players_in_locations,
                                    players_in_traffic=players_in_traffic),
        thumbnail=ipy.EmbedAttachment(url=config.TRUCKERSMP_LOGO),
        url="https://traffic.krashnz.com/",
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        fields=fields,
        footer=ipy.EmbedFooter(
            text="Information provided by TruckyApp",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def location_stats(locations: list, filter_by: str):
    matched_locations = []
    for location in locations:
        if location.name == filter_by:
            matched_locations.append(location)

    description = get_description()


def player_stats(player: Player):
    """Takes a specific player and creates an embed from them"""
    p = player
    joined = utils.datetime_to_discord_str(utils.iso_to_datetime(p.join_date))
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
        banned = utils.datetime_to_discord_str(utils.iso_to_datetime(p.banned_until), "R")
        description += f"> :hammer: **Unbanned:** {banned}\n"
    if p.permissions.is_game_admin:
        description += f"> :red_circle: **Player is an in-game admin!**\n"
        description += f"> :black_circle: **Role:** {p.group_name}\n"
    return ipy.Embed(
        title=f":bust_in_silhouette: TruckersMP | Player Information",
        url=f"https://truckersmp.com/user/{p.id}",
        description=description,
        thumbnail=ipy.EmbedAttachment(url=p.avatar),
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        footer=ipy.EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def events_stats(events: list, list_name: str = "Events", max_size: int = 3):
    desc = None
    fields = []
    for index, event in enumerate(events, 1):
        fields.append(embed_fields.get_event(event))
        if index == max_size:
            break
    if len(fields) <= 0:
        desc = ":slight_frown: No events found!"

    return ipy.Embed(
        title=f":truck: TruckersMP | {list_name}",
        url="https://truckersmp.com/events",
        description=desc,
        thumbnail=ipy.EmbedAttachment(url=config.TRUCKERSMP_LOGO),
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        fields=fields,
        footer=ipy.EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def event_stats(event: Event, avatar: str):
    """Takes a specific event and creates an embed from them"""
    e = event
    start_time = utils.datetime_to_discord_str(utils.iso_to_datetime(e.start_at))
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

    return ipy.Embed(
        title=f"{e.name}",
        url=f"https://truckersmp.com/events/{e.id}",
        images=[ipy.EmbedAttachment(url=e.map)],
        thumbnail=ipy.EmbedAttachment(url=avatar),
        description=description,
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        footer=ipy.EmbedFooter(
            text="Information provided by TruckersMP",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def bot_info(avatar_url, invite_link, privacy_policy, source_code):
    fields = [
        ipy.EmbedField(
            name="About",
            value=f"Hi, I'm Alfie! :wave:\nA small companion for TruckersMP stats.\nThanks for using me :)"
        ),
        ipy.EmbedField(
            name="Commands",
            value=f"I fully support slash commands!\nType **/** in chat for more"
        ),
        ipy.EmbedField(
            name="Useful Links",
            value=f":robot: [Invite]({invite_link}) | "
                  f":shield: [Privacy Policy]({privacy_policy}) | "
                  f":mag: [Source Code]({source_code})"
        )
    ]
    return ipy.Embed(
        title=":page_facing_up: Bot Information",
        fields=fields,
        color=config.EMBED_COLOUR,
        timestamp=ipy.Timestamp.utcnow(),
        footer=ipy.EmbedFooter(
            text="Developed with love by Sam#9210",
            icon_url=config.BOT_AVATAR_URL
        )
    )


def dev_get_guilds(bot, max_length: int = 4000) -> list[str]:
    guilds_descs = []  # creates an array with strings of guild lists, each up to the max_length ready for embed desc
    zfill_length = len(str(len(bot.guilds)))  # Get number of guilds and get length of chars (e.g. 95 is 2 - 9 & 5 = 2)
    guilds_txt_list = [
        f"**{str(i).zfill(zfill_length)}**. {g.id} - {g.name} ({g.member_count})"
        for i, g in enumerate(sorted(bot.guilds, key=lambda x: x.member_count, reverse=True), 1)
    ]
    guilds_txt = ""
    for g in guilds_txt_list:
        if len(guilds_txt) + len(g) > max_length:
            guilds_descs.append(guilds_txt)
            guilds_txt = ""
        guilds_txt += g + "\n"
    guilds_descs.append(guilds_txt)
    return guilds_descs


def dev_get_caches() -> list[ipy.EmbedField]:
    fields = []
    for cache in get_caches():
        c = cache.get_info()
        fields.append(
            ipy.EmbedField(
                name=c.name,
                value=f"*Usage:* **{c.hits}** hits, **{c.misses}** ({c.expired_misses}) misses\n"
                      f"*Size:* **{c.size}** / **{c.max_size}** items\n"
                      f"*TTL:* {str(c.time_to_live)}",
                inline=True
            )
        )
    return fields


def dev_info(bot) -> list[ipy.Embed]:
    embeds = []
    caches_txt = [
        f"{c.name}:  |  {c.hits} / {c.misses} ({c.expired_misses})  |  "
        f"{c.size} / {c.max_size}  |  {str(c.time_to_live)}"
        for c in [c.get_info() for c in get_caches()]

    ]
    descriptions = ["", "", ]
    fields = [  # of the first embed only
        ipy.EmbedField(
            name="Stats",
            value=f"**Guild Count**: {len(bot.guilds)}\n"
        )
    ]
    embeds_fields = [fields, dev_get_caches()]
    descriptions += dev_get_guilds(bot)
    for page, desc in enumerate(descriptions, 1):
        embeds.append(
            ipy.Embed(
                title=f":robot: Dev Information - {'Overview' if page == 1 else 'Caches' if page == 2 else 'Guilds'}",
                description=desc,
                fields=embeds_fields[page-1] if page == 1 or page == 2 else [],
                color=config.EMBED_COLOUR,
                timestamp=ipy.Timestamp.utcnow(),
                footer=ipy.EmbedFooter(
                    text=f"Page {page} / {len(descriptions)}",
                    icon_url=config.BOT_AVATAR_URL
                )
            )
        )
    return embeds
