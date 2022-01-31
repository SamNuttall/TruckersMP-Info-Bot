import interactions
from core import handler as h
from core import command as c
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("APP_TOKEN")
TEST_GUILD_ID = getenv("TEST_GUILD_ID")
bot = interactions.Client(token=TOKEN)


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


@bot.autocomplete(c.get(c.OptionName.SERVER), command=c.get_command(bot, c.Name.SERVERS).id)
async def autocomplete_server(ctx, user_input: str = ""):
    await h.autocomplete_server(ctx, user_input)


@bot.autocomplete(c.get(c.OptionName.LOCATION), command=c.get_command(bot, c.Name.TRAFFIC).id)
async def autocomplete_traffic(ctx, user_input: str = ""):
    await h.autocomplete_traffic(ctx, user_input)


@bot.autocomplete(c.get(c.OptionName.SERVER), command=c.get_command(bot, c.Name.TRAFFIC).id)
async def autocomplete_traffic_servers(ctx, user_input: str = ""):
    await h.autocomplete_traffic_servers(ctx, user_input)


if __name__ == "__main__":
    bot.start()
