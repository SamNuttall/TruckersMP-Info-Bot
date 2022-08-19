import interactions
from interactions import autodefer, MISSING
from core import handler as h
from core import command as c
from core import startup
from os import getenv
from dotenv import load_dotenv
from interactions.base import get_logger
import config
import logging

logging.basicConfig(filename="log.log",
                    level=logging.INFO,
                    format="[%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(funcName)s:%(lineno)s] %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S")
client_logger = get_logger("context")
logger = get_logger("general")
client_logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)

logger.debug("Starting bot")
load_dotenv()
TOKEN = getenv("APP_TOKEN")
STEAM_API_KEY = getenv("STEAM_API_KEY")

if not startup.checks(TOKEN, STEAM_API_KEY, config.GUILD_ID, config.ADMIN_GUILD_ID, config.EPHEMERAL_RESPONSES):
    print("Failed startup checks; Check log file (log.log) for info")
    quit(1)

config.GUILD_ID = config.GUILD_ID if config.GUILD_ID else MISSING

bot = interactions.Client(token=TOKEN,
                          intents=interactions.Intents.GUILD_INTEGRATIONS,
                          presence=interactions.ClientPresence(
                              activities=[interactions.PresenceActivity(
                                  name="TruckersMP Stats", type=interactions.PresenceActivityType.WATCHING)
                              ]
                          ))


@bot.event
async def on_ready():
    await h.on_ready(bot)


@bot.command(
    name=c.Name.SERVERS,
    description=c.Description.SERVERS,
    scope=config.GUILD_ID,
    options=c.Options.SERVERS,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def servers_cmd(ctx: interactions.CommandContext, server: int = None, game: str = None):
    await h.servers_cmd(ctx, server, game)


@bot.command(
    name=c.Name.TRAFFIC,
    description=c.Description.TRAFFIC,
    scope=config.GUILD_ID,
    options=c.Options.TRAFFIC,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def traffic_cmd(ctx: interactions.CommandContext, location: str = None, server: str = None, game: str = None):
    await h.traffic_cmd(ctx, location, server, game)


@bot.command(
    name=c.Name.PLAYER,
    description=c.Description.PLAYER,
    scope=config.GUILD_ID,
    options=c.Options.PLAYER,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def player_cmd(ctx: interactions.CommandContext, id: int = None, name: str = None):
    await h.player_cmd(ctx, id, name, STEAM_API_KEY)


@bot.command(
    name=c.Name.EVENTS,
    description=c.Description.EVENTS,
    scope=config.GUILD_ID,
    options=c.Options.EVENTS,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def events_cmd(ctx: interactions.CommandContext, id: int = None):
    await h.events_cmd(ctx, id)


@bot.command(
    name=c.Name.INFO,
    description=c.Description.INFO,
    scope=config.GUILD_ID,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def info_cmd(ctx: interactions.CommandContext):
    await h.info_cmd(ctx, config)


@bot.command(
    name=c.Name.FEEDBACK,
    description=c.Description.FEEDBACK,
    scope=config.GUILD_ID,
    dm_permission=True
)
@autodefer(ephemeral=config.EPHEMERAL_RESPONSES)
async def feedback_cmd(ctx: interactions.CommandContext):
    await h.feedback_cmd(ctx)


@bot.command(
    name=c.Name.DEV_INFO,
    description=c.Description.DEV_INFO,
    scope=config.ADMIN_GUILD_ID
)
@autodefer(ephemeral=True)
async def devinfo_cmd(ctx: interactions.CommandContext):
    await h.devinfo_cmd(ctx, bot, config.OWNER_ID)


@bot.command(
    name=c.Name.CACHE,
    description=c.Description.CACHE,
    scope=config.ADMIN_GUILD_ID
)
@autodefer(ephemeral=True)
async def cache_cmd(ctx: interactions.CommandContext):
    await h.cache_cmd(ctx, config.OWNER_ID)


@bot.modal("feedback_form")
async def on_feedback_modal(ctx, subject, content):
    await h.on_feedback_modal(ctx, bot, subject, content)


@bot.autocomplete(command=c.Name.SERVERS, name=c.OptionName.SERVER)
async def autocomplete_server(ctx, user_input: str = ""):
    await h.autocomplete_server(ctx, user_input)


@bot.autocomplete(command=c.Name.TRAFFIC, name=c.OptionName.LOCATION)
async def autocomplete_traffic(ctx, user_input: str = ""):
    await h.autocomplete_traffic(ctx, user_input)


@bot.autocomplete(command=c.Name.TRAFFIC, name=c.OptionName.SERVER)
async def autocomplete_traffic_servers(ctx, user_input: str = ""):
    await h.autocomplete_traffic_servers(ctx, user_input)


if __name__ == "__main__":
    bot.start()
