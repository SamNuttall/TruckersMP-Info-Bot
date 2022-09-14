import interactions
from interactions import extension_component, extension_modal, ComponentContext

from core.discord import component as dc
from core.logic import component as lc
from core.public import bot


class ComponentCog(interactions.Extension):

    @extension_component(dc.Button.EVENT_BACK)
    async def event_back_button(self, ctx: ComponentContext):
        await lc.Button.event_back(ctx)

    @extension_component(dc.SelectMenu.EVENTS)
    async def event_lists_selectmenu(self, ctx: ComponentContext, value):
        await lc.SelectMenu.events(ctx, value)

    @extension_component(dc.SelectMenu.EVENTS_SELECTOR)
    async def event_selector_selectmenu(self, ctx: ComponentContext, value):
        await lc.SelectMenu.events_selector(ctx, value)

    @extension_modal("feedback_form")
    async def on_feedback_modal(self, ctx, subject, content):
        await lc.Modal.feedback(ctx, bot, subject, content)


def setup(client):
    ComponentCog(client)
