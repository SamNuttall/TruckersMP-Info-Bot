import interactions
from core import assemble, data
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("APP_TOKEN")
TEST_GUILD_ID = getenv("TEST_GUILD_ID")
bot = interactions.Client(token=TOKEN)


@bot.command(
    name="servers",
    description="Get information about TruckersMP server(s)",
    scope=TEST_GUILD_ID,
    options=[
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="server",
            description="Get information for a specific server only",
            required=False,
            autocomplete=True
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="game",
            description="Get information for servers of a particular game only",
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
)
async def test(ctx: interactions.CommandContext, server: int = None, game: str = None):
    server_id = server
    server_data = await data.get_servers()
    if server_data['error']:
        # Something went wrong
        return
    servers = server_data['servers']
    if not server_id:
        # All servers (possibly filtered by game)
        return
    server = None
    for s in servers:
        if s['id'] == server_id:
            server = s
    if server:
        # Specific server
        return
    # Server not found


@bot.autocomplete("server", command=bot.http.cache.interactions.get("servers").id)
async def autocomplete_servers(ctx, user_input: str = ""):
    servers = await data.get_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


@bot.command(
    name="traffic",
    description="Get information about traffic in-game",
    scope=TEST_GUILD_ID,
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="location",
            description="Get traffic for a specific location only",
            required=False,
            autocomplete=True
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="server",
            description="Get traffic for a specific server only",
            required=False,
            autocomplete=True
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="game",
            description="Get traffic for servers of a particular game only",
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
)
async def test(ctx: interactions.CommandContext, location: str = None, server: str = None, game: str = None):
    return  # Pending implementation


@bot.autocomplete("location", command=bot.http.cache.interactions.get("traffic").id)
async def autocomplete_traffic(ctx, user_input: str = ""):
    traffic_servers = await data.get_traffic_servers()
    if traffic_servers['error']:
        return  # error
    traffic = await data.get_traffic(traffic_servers['servers'])
    if traffic['error']:
        return
    if not traffic['error']:
        await ctx.populate(
            await assemble.get_location_choices(traffic['traffic'], user_input)
        )


@bot.autocomplete("server", command=bot.http.cache.interactions.get("traffic").id)
async def autocomplete_traffic_servers(ctx, user_input: str = ""):
    servers = await data.get_traffic_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


if __name__ == "__main__":
    bot.start()
