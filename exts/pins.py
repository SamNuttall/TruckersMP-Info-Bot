"""
Extension for pins (auto updating messages)
"""

import interactions as ipy

import config
from common.data.db import Pin
from common.discord import command as cmd, permissions
from common.ui import embeds


async def check_sendable(bot: ipy.Client, ctx: ipy.InteractionContext, channel: ipy.GuildChannel):
    """Run a sanity check to ensure the bot can send and edit a message"""
    if not ctx.guild:
        await ctx.send("This command can only be used in a server!", ephemeral=True)
        return False
    perm_data = permissions.check_channel_permissions(bot.user, channel, permissions.SEND_AND_EDIT)
    if not perm_data[0]:
        await ctx.send(embed=embeds.missing_permission(
            f"> **Missing `{permissions.get_name(perm_data[1])}` permissions in {channel.mention}.**\n\n"
            f"To use pins, I need the following permissions in the target channel:\n"
            f"- `View Channel` - So I can see the channel you want to send the message in\n"
            f"- `Send Messages` - I can send the pinned message\n"
            f"- `Read Message History` - I can find and edit the pinned message I sent\n"
        ), ephemeral=True)
        return False
    perm_data = permissions.check_channel_permissions(ctx.author, channel, permissions.SEND_AND_EDIT)
    if not perm_data[0]:
        await ctx.send("The bot cannot setup a pin message in a channel you cannot send messages too!", ephemeral=True)
        return False
    return True


class PinsExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.PINS,
        description=cmd.Description.PINS,
        scopes=[config.ADMIN_GUILD_ID],
        dm_permission=False
    )
    @ipy.slash_default_member_permission(ipy.Permissions.MANAGE_GUILD)
    async def pins_cmd(self, ctx: ipy.InteractionContext):
        ...

    @pins_cmd.subcommand(
        sub_cmd_name=cmd.Name.PINS_ADD,
        sub_cmd_description=cmd.Description.PINS_ADD,
        options=cmd.Options.PINS_ADD,
    )
    async def pins_add_cmd(self, ctx: ipy.InteractionContext, type: int, channel: ipy.GuildChannel = None):
        if channel is None:
            channel = ctx.channel
        if not await check_sendable(self.bot, ctx, channel):
            return  # function sends message
        pin = await Pin.create_and_finish(self.bot, type, ctx.guild_id, channel.id)
        await ctx.send(f":white_check_mark: **Pin created!** Check it out in {channel.mention}.", ephemeral=True)
