import interactions
from interactions import extension_autocomplete

from core.discord import command as cmd
from core.logic import autocomplete as al


class AutocompleteCog(interactions.Extension):

    @extension_autocomplete(command=cmd.Name.SERVERS, name=cmd.OptionName.SERVER)
    async def autocomplete_server(self, ctx, user_input: str = ""):
        await al.server(ctx, user_input)

    @extension_autocomplete(command=cmd.Name.TRAFFIC, name=cmd.OptionName.LOCATION)
    async def autocomplete_traffic(self, ctx, user_input: str = ""):
        await al.traffic(ctx, user_input)

    @extension_autocomplete(command=cmd.Name.TRAFFIC, name=cmd.OptionName.SERVER)
    async def autocomplete_traffic_servers(self, ctx, user_input: str = ""):
        await al.traffic_servers(ctx, user_input)


def setup(client):
    AutocompleteCog(client)
