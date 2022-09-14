import interactions
from interactions import autodefer, extension_command, CommandContext

from core.discord import command as cmd
from core.logic import command as cl
from core.public import bot
from core.public import usr_config as config


class CommandCog(interactions.Extension):
    @extension_command(
        name=cmd.Name.SERVERS,
        description=cmd.Description.SERVERS,
        scope=config.GUILD_ID,
        options=cmd.Options.SERVERS,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def servers(self, ctx: CommandContext, server: int = None, game: str = None):
        await cl.Public.servers(ctx, server, game)

    @extension_command(
        name=cmd.Name.TRAFFIC,
        description=cmd.Description.TRAFFIC,
        scope=config.GUILD_ID,
        options=cmd.Options.TRAFFIC,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def traffic(self, ctx: CommandContext, location: str = None, server: str = None, game: str = None):
        await cl.Public.traffic(ctx, location, server, game)

    @extension_command(
        name=cmd.Name.PLAYER,
        description=cmd.Description.PLAYER,
        scope=config.GUILD_ID,
        options=cmd.Options.PLAYER,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def player(self, ctx: CommandContext, id: int = None, name: str = None):
        await cl.Public.player(ctx, id, name)

    @extension_command(
        name=cmd.Name.EVENTS,
        description=cmd.Description.EVENTS,
        scope=config.GUILD_ID,
        options=cmd.Options.EVENTS,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def events(self, ctx: CommandContext, id: int = None):
        await cl.Public.events(ctx, id)

    @extension_command(
        name=cmd.Name.INFO,
        description=cmd.Description.INFO,
        scope=config.GUILD_ID,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def info(self, ctx: CommandContext):
        await cl.Public.info(ctx, config)

    @extension_command(
        name=cmd.Name.FEEDBACK,
        description=cmd.Description.FEEDBACK,
        scope=config.GUILD_ID,
        dm_permission=True
    )
    @autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
    async def feedback_cmd(self, ctx: CommandContext):
        await cl.Public.feedback(ctx)

    @extension_command(
        name=cmd.Name.DEV_INFO,
        description=cmd.Description.DEV_INFO,
        scope=config.ADMIN_GUILD_ID
    )
    @autodefer(ephemeral=True)
    async def devinfo_cmd(self, ctx: CommandContext):
        await cl.Private.devinfo(ctx, bot, config.OWNER_ID)

    @extension_command(
        name=cmd.Name.CACHE,
        description=cmd.Description.CACHE,
        scope=config.ADMIN_GUILD_ID
    )
    @autodefer(ephemeral=True)
    async def cache_cmd(self, ctx: CommandContext):
        await cl.Private.cache(ctx, config.OWNER_ID)


def setup(client):
    CommandCog(client)
