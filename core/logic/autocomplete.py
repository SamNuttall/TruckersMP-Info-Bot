# Core; Logic: Autocomplete

from truckersmp import exceptions
from truckersmp.base import execute

from core import log, data
from core.discord import choices
from core.public import truckersmp


@log.interaction("autocomplete")
async def server(ctx, user_input: str):
    try:
        servers = await execute(truckersmp.get_servers)
    except exceptions.ExecuteError:
        return  # Will produce a "error loading options" in the Discord client
    await ctx.populate(
        await choices.get_servers(servers, user_input)
    )


@log.interaction("autocomplete")
async def traffic(ctx, user_input: str):
    try:
        servers = await execute(data.get_traffic_servers)
        traffic_data = await execute(data.get_traffic, servers)
    except exceptions.ExecuteError:
        return
    await ctx.populate(
        await choices.get_locations(traffic_data, user_input)
    )


@log.interaction("autocomplete")
async def traffic_servers(ctx, user_input: str):
    try:
        servers = await data.get_traffic_servers()
    except exceptions.ExecuteError:
        return
    await ctx.populate(
        await choices.get_servers(servers, user_input)
    )
