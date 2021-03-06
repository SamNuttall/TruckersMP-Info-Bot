import interactions
from interactions import Option, OptionType
from core import assemble


def get_command(bot: interactions.Client, command_name):
    """
    Get a command from cache using it's name

    Args:
        bot: interactions.Client = The bot client
        command_name: Name = The name of the command
    Returns:
        ApplicationCommand
    """
    return bot._http.cache.interactions.get(
        command_name
    )


class Name:
    SERVERS = "servers"
    TRAFFIC = "traffic"
    PLAYER = "player"
    EVENTS = "events"


class Description:
    SERVERS = "Get information about TruckersMP server(s)"
    TRAFFIC = "Get information about traffic in-game"
    PLAYER = "Get information about a TruckersMP player"
    EVENTS = "Get information about upcoming events on TruckersMP"


class OptionName:
    SERVER = "server"
    GAME = "game"
    LOCATION = "location"
    ID = "id"
    NAME = "name"


class OptionDescription:
    SERVER = "Get information for a specific server only"
    GAME = "Get information for servers of a particular game only"
    LOCATION = "Get traffic for a specific location only"
    TRAFFIC_SERVER = "Get traffic for a specific server only"
    TRAFFIC_GAME = "Get traffic for servers of a particular game only"
    PLAYER_ID = "Search for a player using their TruckersMP or Steam ID"
    PLAYER_NAME = "Search for a player via their name (Experimental: Uses Steam due to TruckersMP limitations)"
    EVENT_ID = "Search for an event using its TruckersMP ID"


class Options:
    SERVERS = [
        Option(
            type=OptionType.INTEGER,
            name=OptionName.SERVER,
            description=OptionDescription.SERVER,
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=OptionName.GAME,
            description=OptionDescription.GAME,
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
    TRAFFIC = [
        Option(
            type=OptionType.STRING,
            name=OptionName.LOCATION,
            description=OptionDescription.LOCATION,
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=OptionName.SERVER,
            description=OptionDescription.TRAFFIC_SERVER,
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=OptionName.GAME,
            description=OptionDescription.TRAFFIC_GAME,
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
    PLAYER = [
        Option(
            type=OptionType.INTEGER,
            name=OptionName.ID,
            description=OptionDescription.PLAYER_ID,
            required=False
        ),
        Option(
            type=OptionType.STRING,
            name=OptionName.NAME,
            description=OptionDescription.PLAYER_NAME,
            required=False
        )
    ]
    EVENTS = [
        Option(
            type=OptionType.INTEGER,
            name=OptionName.ID,
            description=OptionDescription.EVENT_ID,
            required=False
        )
    ]
