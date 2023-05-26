"""
Extension for owner (private/admin) interactions
"""

import interactions as ipy

import config
from common.discord import command as cmd


class AdminExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.DEV_INFO,
        description=cmd.Description.DEV_INFO
    )
    async def devinfo_cmd(self, ctx: ipy.InteractionContext):
        if ctx.author.user.id != config.OWNER_ID:
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return
        # TODO: Implement new devinfo command (which combines /cache)
