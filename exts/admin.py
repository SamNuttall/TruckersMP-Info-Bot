"""
Extension for owner (private/admin) interactions
"""

import interactions as ipy
from interactions.ext.paginators import Paginator

import config
from common.discord import command as cmd
from common.ui import embeds


class AdminExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.DEV_INFO,
        description=cmd.Description.DEV_INFO,
        scopes=[config.ADMIN_GUILD_ID]
    )
    async def devinfo_cmd(self, ctx: ipy.InteractionContext):
        if ctx.author.id not in config.OWNER_ID:
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return

        paginator = Paginator.create_from_embeds(self.bot, *embeds.dev_info(self.bot))
        await paginator.send(ctx, ephemeral=True)

    @ipy.listen(disable_default_listeners=True)
    async def on_command_error(self, event: ipy.api.events.CommandError):
        await event.ctx.send(embed=embeds.unhandled_error(), ephemeral=True)
        await self.bot.on_command_error(self.bot, event)  # call default error handler
