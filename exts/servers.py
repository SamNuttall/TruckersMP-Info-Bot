"""
Extension for TruckersMP server behaviour
"""

import interactions as ipy
from truckersmp import exceptions
from truckersmp.base import execute

import config
from common.const import truckersmp
from common.data import retrieve
from common.discord import choices
from common.discord import command as cmd
from common.ui import retrieve as ui


class ServersExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.SERVERS,
        description=cmd.Description.SERVERS,
        options=cmd.Options.SERVERS,
        dm_permission=True
    )
    async def servers_cmd(self, ctx: ipy.InteractionContext, server: int = None, game: str = None):
        if server and game:
            game = None
        server_id = server

        embeds_func = ui.Servers.singular(self.bot, server_id) if server_id else ui.Servers.overview(self.bot, game)
        await ctx.send(
            embeds=await embeds_func,
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @servers_cmd.autocomplete(cmd.OptionName.SERVER)
    async def autocomplete_server(self, ctx: ipy.AutocompleteContext):
        try:
            servers = await execute(truckersmp.get_servers)
        except exceptions.ExecuteError:
            return  # Will produce a "error loading options" in the Discord client
        await ctx.send(
            choices=await choices.get_servers(servers, ctx.input_text)
        )

    @ipy.Task.create(ipy.TimeTrigger(hour=2, minute=0))  # run daily at 2am
    async def sync_time(self):
        """Time is synced from the API daily and then the actual in-game time is calculated based off the last sync"""
        self.bot.synced_ingame_time = await retrieve.sync_time()

    @ipy.listen()
    async def on_startup(self):
        self.bot.synced_ingame_time = None
        await self.sync_time()  # sync time when bot starts
        self.sync_time.start()
