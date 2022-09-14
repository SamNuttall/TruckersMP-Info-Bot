import interactions
from core.public import Caches

import config
from core.discord import component as dc
from core.interface import base as i


class SelectMenu:
    @staticmethod
    async def events(ctx, value):
        list_type = value[0]
        components = dc.SelectMenu.get_event_lists(default=list_type)
        await ctx.edit(
            embeds=await i.Events.overview(list_type),
            components=components
        )


class Modal:
    @staticmethod
    async def feedback(ctx, bot, subject, content):
        Caches.feedback.add(ctx.author.id, True)
        await ctx.send("Thanks for your feedback!", ephemeral=True)
        channel = await interactions.get(bot, interactions.Channel, object_id=config.FEEDBACK_CHANNEL_ID)
        await channel.send(f"**From:** {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id})"
                           f"\n**Subject:**{subject}\n**Content:**\n{content}")
