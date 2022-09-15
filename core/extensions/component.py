# Core; Extensions: Component

import interactions
from interactions import extension_component, extension_modal, ComponentContext, autodefer
from interactions.ext.persistence import PersistenceExtension, extension_persistent_component

from core.discord import component as dc
from core.logic import component as lc


class ComponentCog(interactions.Extension):

    @extension_component(dc.SelectMenu.EVENTS)
    async def event_lists_selectmenu(self, ctx: ComponentContext, value):
        await lc.SelectMenu.events(ctx, value)

    @extension_component(dc.SelectMenu.EVENTS_SELECTOR)
    async def event_selector_selectmenu(self, ctx: ComponentContext, value):
        await lc.SelectMenu.events_selector(ctx, value)

    @extension_modal("feedback_form")
    async def on_feedback_modal(self, ctx, subject, content):
        await lc.Modal.feedback(ctx, subject, content)


class PersistenceCog(PersistenceExtension):

    @extension_persistent_component(dc.Button.EVENT_BACK)
    async def event_back_btn(self, ctx, list_type):
        await lc.Button.event_back(ctx, list_type)


def setup(client):
    ComponentCog(client)
    PersistenceCog(client)
