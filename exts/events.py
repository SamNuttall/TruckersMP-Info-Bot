"""
Extension for TruckersMP server behaviour
"""

import interactions as ipy

import config
from common.discord import component
from common.discord import command as cmd
from common.ui import retrieve as ui


class EventsExtension(ipy.Extension):

    @ipy.slash_command(
        name=cmd.Name.EVENTS,
        description=cmd.Description.EVENTS,
        options=cmd.Options.EVENTS,
        dm_permission=True
    )
    async def events_cmd(self, ctx: ipy.InteractionContext, id: int = None):
        if id:
            embeds_func = ui.Events.singular(id)
            components = None
        else:
            embeds_func = ui.Events.overview()
            components = ipy.spread_to_rows(
                component.SelectMenu.get_event_lists(),
                await component.SelectMenu.get_event_selector()
            )

        await ctx.send(
            embeds=await embeds_func,
            ephemeral=config.EPHEMERAL_RESPONSES,
            components=components
        )

    # TODO: Add callbacks
