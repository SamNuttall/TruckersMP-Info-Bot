import interactions
from interactions import Option, OptionType
from core import assemble
from enum import Enum


def get(enum):
    """Gets the raw value of any Enum"""
    return enum.value


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
        get(command_name)
    )


class Name(Enum):
    SERVERS = "servers"
    TRAFFIC = "traffic"


class Description(Enum):
    SERVERS = "Get information about TruckersMP server(s)"
    TRAFFIC = "Get information about traffic in-game"


class OptionName(Enum):
    SERVER = "server"
    GAME = "game"
    LOCATION = "location"


class OptionDescription(Enum):
    SERVER = "Get information for a specific server only"
    GAME = "Get information for servers of a particular game only"
    LOCATION = "Get traffic for a specific location only"
    TRAFFIC_SERVER = "Get traffic for a specific server only"
    TRAFFIC_GAME = "Get traffic for servers of a particular game only"


class Options(Enum):
    SERVERS = [
        Option(
            type=OptionType.INTEGER,
            name=get(OptionName.SERVER),
            description=get(OptionDescription.SERVER),
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=get(OptionName.GAME),
            description=get(OptionDescription.GAME),
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
    TRAFFIC = [
        Option(
            type=OptionType.STRING,
            name=get(OptionName.LOCATION),
            description=get(OptionDescription.LOCATION),
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=get(OptionName.SERVER),
            description=get(OptionDescription.TRAFFIC_SERVER),
            required=False,
            autocomplete=True
        ),
        Option(
            type=OptionType.STRING,
            name=get(OptionName.GAME),
            description=get(OptionDescription.TRAFFIC_GAME),
            required=False,
            choices=assemble.get_game_choices()
        )
    ]
