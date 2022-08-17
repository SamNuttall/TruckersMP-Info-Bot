import asyncio
from interactions import CommandContext
from core import assemble, data, embed, format, util
from datetime import datetime
from interactions.base import get_logger
import config
from truckersmp import TruckersMP

logger = get_logger("general")
truckersmp = TruckersMP(logger=logger)


async def servers_cmd(ctx: CommandContext, server: int, game: str):
    logger.debug(f"Handle Command Request: servers, guild {ctx.guild_id}, user {ctx.author.user.id}")
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
    logger.debug(f"Handle Command Request: traffic, guild {ctx.guild_id}, user {ctx.author.user.id}")
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
    """Pending implementation"""


async def cache_cmd(ctx):
    info = util.get_cache_info()
    await ctx.send(f":file_folder: **Caches** | Chars: {len(info)}```{util.get_cache_info()}```", ephemeral=True)


async def autocomplete_server(ctx, user_input: str):
    logger.debug(f"Handle Autocomplete Request: servers, guild {ctx.guild_id}, user {ctx.author.user.id}")
    servers = await data.get_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


async def autocomplete_traffic(ctx, user_input: str):
    logger.debug(f"Handle Autocomplete Request: traffic, guild {ctx.guild_id}, user {ctx.author.user.id}")
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
    logger.debug(f"Handle Autocomplete Request: traffic_servers, guild {ctx.guild_id}, user {ctx.author.user.id}")
    servers = await data.get_traffic_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


async def on_ready(bot):
    ready_string = f"Ready; Logged in as {bot.me.name}"
    logger.info(ready_string + f" (ID: {bot.me.id})")
    print(ready_string)
