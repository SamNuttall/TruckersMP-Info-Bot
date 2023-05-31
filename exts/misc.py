"""
Extension for public but miscellaneous interactions
"""

import interactions as ipy

import config
from common.const import Caches
from common.discord import component
from common.discord import command as cmd
from common.ui import embeds


class MiscExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.INFO,
        description=cmd.Description.INFO,
        dm_permission=True
    )
    async def info_cmd(self, ctx: ipy.InteractionContext):
        await ctx.send(
            embeds=embeds.bot_info(
                config.BOT_AVATAR_URL,
                config.BOT_INVITE_URL,
                config.PRIVACY_POLICY_URL,
                config.SOURCE_CODE_URL
            ),
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @ipy.slash_command(
        name=cmd.Name.FEEDBACK,
        description=cmd.Description.FEEDBACK,
        dm_permission=True
    )
    async def feedback_cmd(self, ctx: ipy.SlashContext):
        if Caches.feedback.get(ctx.author.id) is not None:
            await ctx.send("You have already sent feedback within the last 24 hours. Try again later.", ephemeral=True)
            return
        await ctx.send_modal(modal=component.Modal.feedback)

    @ipy.modal_callback("feedback_form")
    async def feedback_modal_callback(self, ctx: ipy.ModalContext, subject_input, content_input):
        Caches.feedback.add(ctx.author.id, True)
        await ctx.send("Thanks for your feedback!", ephemeral=True)
        channel = await self.bot.fetch_channel(config.FEEDBACK_CHANNEL_ID)
        await channel.send(
            f"**From:** {ctx.user.tag} ({ctx.user.id})\n"
            f"**Subject:** {subject_input}\n"
            f"**Content:**\n{content_input}"
        )
