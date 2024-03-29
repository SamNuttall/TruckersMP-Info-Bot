"""
Defines classes to create a data model of what we expect an API to return.
Models here are only for non async-truckersmp related objects or to aid the visualisation of data.
Functions defined here aid the creation of models, often by adding more data.
"""

import re

from common.ui.emoji import Emoji, TRAFFIC_SEVERITY
from common import utils


class TrafficServerAttributes:
    """Stores the attributes (even if not used) of a traffic server"""
    name = "name"  # str
    url = "url"  # str
    short_name = "short"  # str
    game = "game"  # str


class LocationAttributes:
    """Stores the attributes (even if not used) of a location"""
    name = "name"  # str
    players = "players"  # int
    country = "country"  # str
    severity = "severity"  # str
    color = "color"  # str
    colour = "color"  # str
    average_speed = "averageSpeed"  # int
    new_severity = "newSeverity"  # str
    traffic_jams = "trafficJams"  # int
    players_in_traffic_jams = "playersInvolvedInTrafficJams"  # int
    layer_id = "layerID"  # str
    server = "server"  # dict (added by self)
    game = "game"  # str (added by self)


class ServerType:
    """Unofficial way of storing the type of server."""
    simulation = "Simulation"
    arcade = "Arcade"
    community_event = "Community Event"
    official_event = "Official Event"
    unknown = "Unknown"


def get_server_type(name: str, is_event: bool = False):
    """
    Get a servers "type" depending on it's name.
    This shouldn't be relied for anything vital and may be inaccurate, especially if TruckersMP changes server names.

    Returns:
        ServerType: str
    """
    if not is_event:
        simulation_names = ("simulation", "promods")  # regex
        arcade_names = ("arcade",)  # regex
        is_simulation_check = any(re.search(sim_name, name.lower()) for sim_name in simulation_names)
        is_arcade_match = any(re.search(arc_name, name.lower()) for arc_name in arcade_names)
        if is_arcade_match:  # First as "promods arcade" also passes sim check
            return ServerType.arcade
        if is_simulation_check:
            return ServerType.simulation
        return ServerType.unknown
    official_names = ("^real operations", "^truckersmp official")  # regex
    is_official_check = any(re.search(official_name, name.lower()) for official_name in official_names)
    if is_official_check:
        return ServerType.official_event
    return ServerType.community_event


class TrafficServer:
    def __init__(self, server):
        self.name = server[TrafficServerAttributes.name]
        self.url = server[TrafficServerAttributes.url]
        self.short_name = server[TrafficServerAttributes.short_name]
        self.game = server[TrafficServerAttributes.game]


class Server:
    """Add format attributes of a specific server ready for use in embeds"""
    def __init__(self, server,
                 online_str="Online",
                 offline_str="Offline",
                 players_if_offline_str="N/A",
                 queue_if_offline_str="N/A",
                 promods_if_disabled=""
                 ):
        self.is_online = server.online
        self.game = server.game.upper()
        self.status_emoji = Emoji.UP if self.is_online else Emoji.DOWN
        self.game_emoji = Emoji.ETS2 if self.game == "ETS2" else Emoji.ATS
        self.status = online_str if self.is_online else offline_str
        self.queue = server.queue if self.is_online else queue_if_offline_str

        self.short_name = server.short_name
        self.name = server.name
        self.is_event = server.event
        self.type = get_server_type(self.name, self.is_event)

        self.formatted_name = self.short_name
        if self.is_event:
            self.formatted_name = utils.trim_string(self.name)

        self.current_players = server.players
        self.max_players = server.max_players
        self.percent_players = int((self.current_players / self.max_players) * 100)
        self.players = f"{self.current_players}/{self.max_players}"
        if not self.is_online:
            self.players = players_if_offline_str

        self.speed_limiter = server.speed_limiter
        self.collisions = server.collisions
        self.cars_for_players = server.cars_for_players
        self.afk_enabled = server.afk_enabled
        self.promods = server.promods

        self.speed_limiter_icon = Emoji.SL_ON if self.speed_limiter else Emoji.SL_OFF
        self.collisions_icon = Emoji.CO_ON if self.collisions else Emoji.CO_OFF
        self.cars_for_players_icon = Emoji.CA_ON if self.cars_for_players else Emoji.CA_OFF
        self.afk_enabled_icon = Emoji.AFK_ON if self.afk_enabled else Emoji.AFK_OFF
        self.promods_icon = Emoji.PM if self.promods else promods_if_disabled

        self.icons = (
            self.speed_limiter_icon, self.collisions_icon,
            self.cars_for_players_icon, self.afk_enabled_icon,
            self.promods_icon
        )


class Location:
    def __init__(self, location):
        self.server = location[LocationAttributes.server]
        self.name = location[LocationAttributes.name]
        self.trimmed_name = utils.trim_string(self.name, 17)
        self.game = location[LocationAttributes.game].upper()
        self.game_emoji = Emoji.ETS2 if self.game == "ETS2" else Emoji.ATS
        self.players = location[LocationAttributes.players]

        self.severity = location[LocationAttributes.severity]
        self.severity_icon = TRAFFIC_SEVERITY[self.severity][0]
        self.severity_bar = TRAFFIC_SEVERITY[self.severity][1]

        self.server_name = self.server[TrafficServerAttributes.name]
        self.trimmed_server_name = utils.trim_string(self.server_name, 12)
        self.server_short_name = self.server[TrafficServerAttributes.short_name]

        self.server_formatted_name = self.server_short_name
        if "event" in self.server[TrafficServerAttributes.url]:
            self.server_formatted_name = utils.trim_string(self.server_name, 9)
