# Core; Extensions: Event

import interactions
from interactions import extension_listener

from core import startup
from core.public import bot


class EventCog(interactions.Extension):

    @extension_listener
    async def on_ready(self):
        await startup.on_ready(bot)


def setup(client):
    EventCog(client)
