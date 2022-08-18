import asyncio
import sys
from interactions import CommandContext
from core import assemble, data, embed, format, util
from datetime import datetime
from interactions.base import get_logger
import config
from truckersmp import TruckersMP

logger = get_logger("general")
truckersmp = TruckersMP(logger=logger)


def log(ctx, name, is_cmd: bool = True):
    req_type = "Command" if is_cmd else "Autocomplete"
    guild = ctx.guild_id if ctx.guild_id else "N/A (Direct Msg)"
    author = ctx.author.user.id if ctx.author else "Unknown"
    logger.debug(f"Handle {req_type} Request: {name} | guild: {guild} & user: {author}")


async def servers_cmd(ctx: CommandContext, server: int, game: str):
    log(ctx, "servers")

    if server and game:
        game = None

    server_id = server
    servers, ingame_time = await asyncio.gather(
        truckersmp.get_servers(), data.get_ingame_time()
    )
    if servers is None:
        logger.error("Returned something went wrong message to user: no servers found")
        await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    if not server_id:
        await ctx.send(
            embeds=await embed.servers_stats(servers, game, await format.format_time(ingame_time)),
            ephemeral=config.EPHEMERAL_RESPONSES
        )
        return
    server = None
    for s in servers:
        if s.id == server_id:
            server = s
    if server:
        await ctx.send(embeds=await embed.server_stats(server, await format.format_time(ingame_time)),
                       ephemeral=config.EPHEMERAL_RESPONSES)
        return
    await ctx.send(embeds=await embed.item_not_found("Specified TruckersMP server"),
                   ephemeral=config.EPHEMERAL_RESPONSES)


async def traffic_cmd(ctx, location: str, server: str, game: str):
    log(ctx, "traffic")

    if server and game:
        game = None

    traffic_servers = await data.get_traffic_servers()
    if traffic_servers['error']:
        logger.error("Returned something went wrong message to user: get traffic servers failed")
        await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    traffic = await data.get_traffic(traffic_servers['servers'])
    if traffic['error']:
        logger.error("Returned something went wrong message to user: get traffic failed")
        await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    await ctx.send(embeds=await embed.traffic_stats(traffic['traffic'], server, game, location),
                   ephemeral=config.EPHEMERAL_RESPONSES)


async def player_cmd(ctx, player_id: int, player_name: str, steam_key):
    log(ctx, "player")

    if player_name:
        steam_id = await data.get_steamid_via_vanityurl(steam_key, player_name)
        if steam_id['error']:
            await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
            return
        steam_id = steam_id['steam_id']
        if steam_id is None:
            desc = "Steam user not found with that Vanity URL"
            await ctx.send(embeds=await embed.item_not_found_detailed("Player", desc),
                           ephemeral=config.EPHEMERAL_RESPONSES)
        player_id = steam_id
    player = await truckersmp.get_player(player_id)
    if player is False:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    elif player is None:
        if player_name:
            desc = f"A Steam [user](https://steamcommunity.com/profiles/{player_id}) was, but they are " \
                   "not a TruckersMP player"
            await ctx.send(embeds=await embed.item_not_found_detailed("Player", desc),
                           ephemeral=config.EPHEMERAL_RESPONSES)
            return
        await ctx.send(embeds=await embed.item_not_found("Player"), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    await ctx.send(embeds=await embed.player_stats(player), ephemeral=config.EPHEMERAL_RESPONSES)


async def events_cmd(ctx, event_id: int):
    log(ctx, "events")

    if event_id:
        event = await truckersmp.get_event(event_id)
        if event is False:
            await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
            return
        elif event is None:
            await ctx.send(embeds=await embed.item_not_found("Event"), ephemeral=config.EPHEMERAL_RESPONSES)
            return
        await ctx.send(embeds=await embed.event_stats(event), ephemeral=config.EPHEMERAL_RESPONSES)
        return
    else:
        events = await truckersmp.get_events()
        if events is False:
            await ctx.send(embeds=await embed.generic_error(), ephemeral=config.EPHEMERAL_RESPONSES)
            return
        elif events is None:
            await ctx.send(embeds=await embed.item_not_found("Events"), ephemeral=config.EPHEMERAL_RESPONSES)
            return
        await ctx.send(embeds=await embed.events_stats(events.featured), ephemeral=config.EPHEMERAL_RESPONSES)


async def info_cmd(ctx, conf):
    log(ctx, "info")
    await ctx.send(embeds=await embed.bot_info(conf.BOT_AVATAR_URL, conf.BOT_INVITE_URL,
                                               conf.PRIVACY_POLICY_URL, conf.SOURCE_CODE_URL),
                   ephemeral=config.EPHEMERAL_RESPONSES)


async def devinfo_cmd(ctx, bot, owner_id):
    log(ctx, "devinfo")
    if ctx.author.user.id != owner_id:
        await ctx.send("You do not have permission to use this command.", ephemeral=True)
        return
    content = ("```"
               f"Num of Guilds: {len(bot.guilds)}\n"
               f"Py Version: {sys.version}"
               "```"
               )
    await ctx.send(content, ephemeral=True)


async def cache_cmd(ctx, owner_id):
    log(ctx, "cache")
    if ctx.author.user.id != owner_id:
        await ctx.send("You do not have permission to use this command.", ephemeral=True)
        return
    info = util.get_cache_info()
    await ctx.send(f":file_folder: **Caches** | Chars: {len(info)}```{util.get_cache_info()}```", ephemeral=True)


async def autocomplete_server(ctx, user_input: str):
    log(ctx, "server", is_cmd=False)
    servers = await truckersmp.get_servers()
    if servers is not None:
        await ctx.populate(
            await assemble.get_server_choices(servers, user_input)
        )


async def autocomplete_traffic(ctx, user_input: str):
    log(ctx, "traffic", is_cmd=False)
    traffic_servers = await data.get_traffic_servers()
    if traffic_servers['error']:
        return  # error
    traffic = await data.get_traffic(traffic_servers['servers'])
    if traffic['error']:
        return
    if not traffic['error']:
        await ctx.populate(
            await assemble.get_location_choices(traffic['traffic'], user_input)
        )


async def autocomplete_traffic_servers(ctx, user_input: str):
    log(ctx, "traffic_servers", is_cmd=False)
    servers = await data.get_traffic_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


async def on_ready(bot):
    ready_string = f"Ready; Logged in as {bot.me.name}"
    logger.info(ready_string + f" (ID: {bot.me.id})")
    print(ready_string)
