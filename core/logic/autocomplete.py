# Core; Logic: Autocomplete

from truckersmp import exceptions
from truckersmp.base import execute

from core import log, data
from core.discord import choices
from core.public import truckersmp


async def server(ctx, user_input: str):
    log.interaction(ctx, "server", is_cmd=False)
    try:
        servers = await execute(truckersmp.get_servers)
    except exceptions.ExecuteError:
        return  # Will produce a "error loading options" in the Discord client
    await ctx.populate(
        await choices.get_servers(servers, user_input)
    )


async def traffic(ctx, user_input: str):
    log.interaction(ctx, "traffic", is_cmd=False)
    try:
        servers = await execute(data.get_traffic_servers)
        traffic_data = await execute(data.get_traffic, servers)
    except exceptions.ExecuteError:
        return
    await ctx.populate(
        await choices.get_locations(traffic_data, user_input)
    )


async def traffic_servers(ctx, user_input: str):
    log.interaction(ctx, "traffic_servers", is_cmd=False)
    try:
        servers = await data.get_traffic_servers()
    except exceptions.ExecuteError:
        return
    await ctx.populate(
        await choices.get_servers(servers, user_input)
    )
