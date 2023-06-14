"""
Extension for TruckersMP server behaviour
"""
import re

import interactions as ipy

import config
from common import utils
from common.discord import component
from common.discord import command as cmd
from common.ui import retrieve as ui, embeds


class EventsExtension(ipy.Extension):

    @staticmethod
    async def get_event_overview_components(list_name: str | None):
        event_lists = component.SelectMenu.get_event_lists(list_name)
        events = await component.SelectMenu.get_events(list_name)
        if events:  # if None, then no events in list
            return ipy.spread_to_rows(event_lists, events)
        return event_lists

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
            components = await self.get_event_overview_components(None)

        await ctx.send(
            embeds=await embeds_func,
            ephemeral=config.EPHEMERAL_RESPONSES,
            components=components
        )

    @ipy.component_callback(component.SelectMenu.EVENT_LISTS_ID)
    async def events_list_callback(self, ctx: ipy.ComponentContext):
        if not utils.is_component_author(ctx):
            return await ctx.send(embed=embeds.cannot_use_component(), ephemeral=True)
        list_name = ctx.values[0]  # featured, upcoming etc
        await ctx.edit_origin(
            embeds=await ui.Events.overview(list_name),
            components=await self.get_event_overview_components(list_name)
        )

    @ipy.component_callback(component.SelectMenu.EVENTS_ID)
    async def events_callback(self, ctx: ipy.ComponentContext):
        if not utils.is_component_author(ctx):
            return await ctx.send(embed=embeds.cannot_use_component(), ephemeral=True)
        event_id, list_name = ctx.values[0].split('#')
        await ctx.edit_origin(
            embeds=await ui.Events.singular(event_id),
            components=component.Button.get_event_back(list_name)
        )

    @ipy.component_callback(re.compile(component.Button.EVENT_BACK_ID + r"#.*"))
    async def event_back_callback(self, ctx: ipy.ComponentContext):
        if not utils.is_component_author(ctx):
            return await ctx.send(embed=embeds.cannot_use_component(), ephemeral=True)
        _, list_name = ctx.custom_id.split('#')
        await ctx.edit_origin(
            embeds=await ui.Events.overview(list_name),
            components=await self.get_event_overview_components(list_name)
        )
