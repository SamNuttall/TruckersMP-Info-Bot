import asyncio
from interactions import CommandContext
from core import assemble, data, embed


async def servers_cmd(ctx: CommandContext, server: int, game: str):
    server_id = server
    server_data, time_data = await asyncio.gather(data.get_servers(), data.get_ingame_time())
    if server_data['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    servers = server_data['servers']
    ingame_time = None
    if not time_data['error']:
        ingame_time = time_data['time']
    if not server_id:
        await ctx.send(embeds=await embed.servers_stats(servers, game, ingame_time), ephemeral=True)
        return
    server = None
    for s in servers:
        if s['id'] == server_id:
            server = s
    if server:
        await ctx.send(embeds=await embed.server_stats(server), ephemeral=True)
        return
    await ctx.send(embeds=await embed.item_not_found("Specified TruckersMP server"), ephemeral=True)


async def traffic_cmd(ctx, location: str, server: str, game: str):
    traffic_servers = await data.get_traffic_servers()
    if traffic_servers['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    traffic = await data.get_traffic(traffic_servers['servers'])
    if traffic['error']:
        await ctx.send(embeds=await embed.generic_error(), ephemeral=True)
        return
    if not location:
        await ctx.send(embeds=await embed.traffic_stats(traffic['traffic'], server, game), ephemeral=True)
        return


async def autocomplete_server(ctx, user_input: str):
    servers = await data.get_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


async def autocomplete_traffic(ctx, user_input: str):
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
    servers = await data.get_traffic_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )
