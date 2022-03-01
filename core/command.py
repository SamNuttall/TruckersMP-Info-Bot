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


class Description:
    SERVERS = "Get information about TruckersMP server(s)"
    TRAFFIC = "Get information about traffic in-game"


class OptionName:
    SERVER = "server"
    GAME = "game"
    LOCATION = "location"


class OptionDescription:
    SERVER = "Get information for a specific server only"
    GAME = "Get information for servers of a particular game only"
    LOCATION = "Get traffic for a specific location only"
    TRAFFIC_SERVER = "Get traffic for a specific server only"
    TRAFFIC_GAME = "Get traffic for servers of a particular game only"


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
