"""
Extension for TruckersMP server behaviour
"""

import interactions as ipy

import config
from common.discord import command as cmd
from common.ui import retrieve as ui


class PlayersExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.PLAYER,
        description=cmd.Description.PLAYER,
        options=cmd.Options.PLAYER,
        dm_permission=True
    )
    async def player_cmd(self, ctx: ipy.InteractionContext, id: int = None, name: str = None):
        await ctx.send(
            embeds=await ui.Player.singular(id, name),
            ephemeral=config.EPHEMERAL_RESPONSES
        )
