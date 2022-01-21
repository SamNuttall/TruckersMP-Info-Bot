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
            name="name",
            description="Get information for a specific server only",
            required=False,
            autocomplete=True
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="game",
            description="Get information for servers of a particular game only",
            required=False,
            autocomplete=True
        )
    ]
)
async def test(ctx: interactions.CommandContext, name: int = None, game: str = None):
    server_id = name
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


@bot.autocomplete("name", command=bot.http.cache.interactions.get("servers").id)
async def autocomplete_servers(ctx, user_input: str = ""):
    servers = await data.get_servers()
    if not servers['error']:
        await ctx.populate(
            await assemble.get_server_choices(servers['servers'], user_input)
        )


@bot.autocomplete("game", command=bot.http.cache.interactions.get("servers").id)
async def autocomplete_games(ctx, user_input: str = ""):
    return  # Pending implementation


if __name__ == "__main__":
    bot.start()
