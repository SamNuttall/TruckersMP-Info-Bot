import interactions
from core import handler as h
from core import command as c
from core import startup
from os import getenv
from dotenv import load_dotenv
from interactions.base import get_logger
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
TEST_GUILD_ID = int(getenv("TEST_GUILD_ID"))

bot = interactions.Client(token=TOKEN)

if not startup.checks(TOKEN):
    print("Failed startup checks; Check log file for info")
    quit(1)


@bot.event
async def on_ready():
    await h.on_ready(bot)


@bot.command(
    name=c.get(c.Name.SERVERS),
    description=c.get(c.Description.SERVERS),
    scope=TEST_GUILD_ID,
    options=c.get(c.Options.SERVERS)
)
async def servers_cmd(ctx: interactions.CommandContext, server: int = None, game: str = None):
    await h.servers_cmd(ctx, server, game)


@bot.command(
    name=c.get(c.Name.TRAFFIC),
    description=c.get(c.Description.TRAFFIC),
    scope=TEST_GUILD_ID,
    options=c.get(c.Options.TRAFFIC)
)
async def traffic_cmd(ctx: interactions.CommandContext, location: str = None, server: str = None, game: str = None):
    await h.traffic_cmd(ctx, location, server, game)


@bot.autocomplete(command=c.get(c.Name.SERVERS), name=c.get(c.OptionName.SERVER))
async def autocomplete_server(ctx, user_input: str = ""):
    await h.autocomplete_server(ctx, user_input)


@bot.autocomplete(command=c.get(c.Name.TRAFFIC), name=c.get(c.OptionName.LOCATION))
async def autocomplete_traffic(ctx, user_input: str = ""):
    await h.autocomplete_traffic(ctx, user_input)


@bot.autocomplete(command=c.get(c.Name.TRAFFIC), name=c.get(c.OptionName.SERVER))
async def autocomplete_traffic_servers(ctx, user_input: str = ""):
    await h.autocomplete_traffic_servers(ctx, user_input)


if __name__ == "__main__":
    try:
        bot.start()
    except KeyboardInterrupt:
        # logger.info("Cleaning up before exit")
        logger.info("Bot shutdown")
        quit()
