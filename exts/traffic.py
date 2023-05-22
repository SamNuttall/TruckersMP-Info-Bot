"""
Extension for TruckersMP traffic behavour
"""

import interactions as ipy
from truckersmp import exceptions
from truckersmp.base import execute

import config
from common.data import retrieve as data
from common.discord import choices
from common.discord import command as cmd
from common.ui import retrieve as ui


class TrafficExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.TRAFFIC,
        description=cmd.Description.TRAFFIC,
        options=cmd.Options.TRAFFIC,
        dm_permission=True
    )
    async def traffic_cmd(self, ctx: ipy.InteractionContext, location: str = None, server: str = None, game: str = None):
        if server and game:
            game = None

        await ctx.send(
            embeds=await ui.Traffic.overview(location, server, game),
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @traffic_cmd.autocomplete(cmd.OptionName.LOCATION)
    async def autocomplete_traffic_location(self, ctx: ipy.AutocompleteContext):
        try:
            servers = await execute(data.get_traffic_servers)
            traffic_data = await execute(data.get_traffic, servers)
        except exceptions.ExecuteError:
            return
        await ctx.send(
            choices=await choices.get_locations(traffic_data, ctx.input_text)
        )

    @traffic_cmd.autocomplete(cmd.OptionName.SERVER)
    async def autocomplete_traffic_server(self, ctx: ipy.AutocompleteContext):
        try:
            servers = await data.get_traffic_servers()
        except exceptions.ExecuteError:
            return
        await ctx.send(
            choices=await choices.get_servers(servers, ctx.input_text)
        )
