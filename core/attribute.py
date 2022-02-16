from enum import Enum
from typing import Union


class Server(Enum):
    """Stores the attributes (even if not used) of a server"""
    id = "id"  # int
    game = "game"  # str
    ip = "ip"  # str
    port = "port"  # int
    name = "name"  # str
    short_name = "shortname"  # str
    id_prefix = "idprefix"  # str
    online = "online"  # bool
    players = "players"  # int
    queue = "queue"  # int
    max_players = "maxplayers"  # int
    map_id = "mapid"  # int
    display_order = "displayorder"  # int
    speed_limiter = "speedlimiter"  # int
    collisions = "collisions"  # bool
    cars_for_players = "carsforplayers"  # bool
    police_cars_for_players = "policecarsforplayers"  # bool
    afk_enabled = "afkenabled"  # bool
    event = "event"  # bool
    special_event = "specialEvent"  # bool
    promods = "promods"  # bool
    sync_delay = "syncdelay"  # int


class TrafficServer(Enum):
    """Stores the attributes (even if not used) of a traffic server"""
    name = "name"  # str
    url = "url"  # str
    short_name = "short"  # str
    game = "game"  # str


class Location(Enum):
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


def get(attribute: Union[Server, TrafficServer, Location]):
    """Gets the raw value of an attribute"""
    return attribute.value
