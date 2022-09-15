# Core; Logic: Component

import interactions
from interactions.ext.persistence import PersistentCustomID

from core import log
from core.public import bot, Caches

import config
from core.discord import component as dc
from core.interface import base as i


class Button:
    @staticmethod
    @log.interaction("button")
    async def event_back(ctx, list_type):
        await ctx.edit(
            embeds=await i.Events.overview(list_type),
            components=interactions.spread_to_rows(
                dc.SelectMenu.get_event_lists(list_type),
                await dc.SelectMenu.get_event_selector(list_type)
            )
        )


class SelectMenu:
    @staticmethod
    @log.interaction("selectMenu")
    async def events(ctx, value):
        list_type = value[0]
        components = interactions.spread_to_rows(
                dc.SelectMenu.get_event_lists(default=list_type),
                await dc.SelectMenu.get_event_selector(list_type)
        )
        await ctx.edit(
            embeds=await i.Events.overview(list_type),
            components=components
        )

    @staticmethod
    @log.interaction("selectMenu")
    async def events_selector(ctx, value):
        event_id, list_type = value[0].split('#')
        await ctx.edit(
            embeds=await i.Events.singular(event_id),
            components=interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="Go Back to Overview",
                emoji=interactions.Emoji(name="🗓️"),
                custom_id=str(PersistentCustomID(
                            bot,
                            dc.Button.EVENT_BACK,
                            list_type
                ))
            )
        )


class Modal:
    @staticmethod
    @log.interaction("modal")
    async def feedback(ctx, subject, content):
        Caches.feedback.add(ctx.author.id, True)
        await ctx.send("Thanks for your feedback!", ephemeral=True)
        channel = await interactions.get(bot, interactions.Channel, object_id=config.FEEDBACK_CHANNEL_ID)
        await channel.send(f"**From:** {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id})"
                           f"\n**Subject:**{subject}\n**Content:**\n{content}")
