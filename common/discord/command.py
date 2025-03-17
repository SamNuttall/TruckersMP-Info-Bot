"""
Stores attributes which are used for commands, such as decorators for slash options
"""

import interactions as ipy

from common.discord import choices


class Name:
    SERVERS = "servers"
    TRAFFIC = "traffic"
    PLAYER = "player"
    EVENTS = "events"
    CACHE = "cache"
    INFO = "info"
    DEV_INFO = "devinfo"
    FEEDBACK = "feedback"
    PINS = "pins"
    PINS_ADD = "add"
    PINS_REMOVE = "remove"


class Description:
    SERVERS = "Get information about TruckersMP server(s)"
    TRAFFIC = "Get information about traffic in-game"
    PLAYER = "Get information about a TruckersMP player"
    EVENTS = "Get information about upcoming events on TruckersMP"
    CACHE = "Get information about the caches (admin)"
    INFO = "Get information about the bot"
    DEV_INFO = "Get information about the bot backend (admin)"
    FEEDBACK = "Give feedback to the bot developer (opens a form, max submission of one a day)"
    PINS = "Manage this server's pins - an automatically updating message."
    PINS_ADD = "Add a pin to this server - an automatically updating message."
    PINS_REMOVE = "Remove a pin from this server - normally, happens automatically if the bot's pin message is deleted."


class OptionName:
    SERVER = "server"
    GAME = "game"
    LOCATION = "location"
    ID = "id"
    NAME = "name"
    PIN_TYPE = "type"
    PIN_CHANNEL = "channel"
    PIN = "pin"


class OptionDescription:
    SERVER = "Get information for a specific server only"
    GAME = "Get information for servers of a particular game only"
    LOCATION = "Get traffic for a specific location only"
    TRAFFIC_SERVER = "Get traffic for a specific server only"
    TRAFFIC_GAME = "Get traffic for servers of a particular game only"
    PLAYER_ID = "Search for a player using their TruckersMP or Steam ID"
    PLAYER_NAME = "Search for a player via their name (Experimental: Uses Steam due to TruckersMP limitations)"
    EVENT_ID = "Search for an event using its TruckersMP ID"
    PIN_TYPE = "Select a pin type, which determines what is sent and kept updated"
    PIN_CHANNEL = "Select a text channel for where the pin will be sent (default: this channel)"
    GUILD_PINS = "Select a pin within the server"


class Options:
    SERVERS = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.INTEGER,
            name=OptionName.SERVER,
            description=OptionDescription.SERVER,
            required=False,
            autocomplete=True
        ),
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,
            name=OptionName.GAME,
            description=OptionDescription.GAME,
            required=False,
            choices=choices.get_games()
        )
    ]
    TRAFFIC = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,
            name=OptionName.LOCATION,
            description=OptionDescription.LOCATION,
            required=False,
            autocomplete=True
        ),
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,
            name=OptionName.SERVER,
            description=OptionDescription.TRAFFIC_SERVER,
            required=False,
            autocomplete=True
        ),
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,
            name=OptionName.GAME,
            description=OptionDescription.TRAFFIC_GAME,
            required=False,
            choices=choices.get_games()
        )
    ]
    PLAYER = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,  # SteamID is too big for an integer
            name=OptionName.ID,
            description=OptionDescription.PLAYER_ID,
            required=False
        ),
        ipy.SlashCommandOption(
            type=ipy.OptionType.STRING,
            name=OptionName.NAME,
            description=OptionDescription.PLAYER_NAME,
            required=False
        )
    ]
    EVENTS = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.INTEGER,
            name=OptionName.ID,
            description=OptionDescription.EVENT_ID,
            required=False
        )
    ]
    PINS_ADD = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.INTEGER,
            name=OptionName.PIN_TYPE,
            description=OptionDescription.PIN_TYPE,
            required=True,
            choices=choices.get_pin_types()
        ),
        ipy.SlashCommandOption(
            type=ipy.OptionType.CHANNEL,
            name=OptionName.PIN_CHANNEL,
            channel_types=[ipy.ChannelType.GUILD_TEXT],
            description=OptionDescription.PIN_CHANNEL,
            required=False
        )
    ]
    PINS_REMOVE = [
        ipy.SlashCommandOption(
            type=ipy.OptionType.INTEGER,
            name=OptionName.PIN,
            description=OptionDescription.GUILD_PINS,
            required=True,
            autocomplete=True
        )
    ]
