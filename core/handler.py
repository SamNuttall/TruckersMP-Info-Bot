import asyncio
from interactions import CommandContext
from core import assemble, data, embed, format
from datetime import datetime
from interactions.base import get_logger

logger = get_logger("general")


async def servers_cmd(ctx: CommandContext, server: int, game: str):
    logger.debug(f"Handle Command Request: servers, guild {ctx.guild_id}, user {ctx.author.user.id}")
    server_id = server
    server_data, time_data = await asyncio.gather(data.get_servers(), data.get_ingame_time())
    if server_data['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    servers = server_data['servers']
    ingame_time = None
    if type(time_data) == datetime:
        ingame_time = await format.format_time(time_data)
    else:
        if not time_data['error']:
            ingame_time = await format.format_time(time_data['time'])
    if not server_id:
        await ctx.send(embeds=await embed.servers_stats(servers, game, ingame_time), ephemeral=True)
        return
    server = None
    for s in servers:
        if s['id'] == server_id:
            server = s
    if server:
        await ctx.send(embeds=await embed.server_stats(server, ingame_time), ephemeral=True)
        return
    await ctx.send(embeds=await embed.item_not_found("Specified TruckersMP server"), ephemeral=True)


async def traffic_cmd(ctx, location: str, server: str, game: str):
    logger.debug(f"Handle Command Request: traffic, guild {ctx.guild_id}, user {ctx.author.user.id}")
    traffic_servers = await data.get_traffic_servers()
    if traffic_servers['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    traffic = await data.get_traffic(traffic_servers['servers'])
    if traffic['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    await ctx.send(embeds=await embed.traffic_stats(traffic['traffic'], server, game, location), ephemeral=True)


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
