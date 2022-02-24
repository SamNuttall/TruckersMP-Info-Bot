from core.emoji import Emoji, TRAFFIC_SEVERITY
from core import util


class Server:
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


class TrafficServer:
    """Stores the attributes (even if not used) of a traffic server"""
    name = "name"  # str
    url = "url"  # str
    short_name = "short"  # str
    game = "game"  # str


class Location:
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


class ServerAttributes:
    """Format the attributes of a specific server ready for use in embeds"""

    def __init__(self, server,
                 online_str="Online",
                 offline_str="Offline",
                 players_if_offline_str="N/A",
                 queue_if_offline_str="N/A",
                 promods_if_disabled=""
                 ):
        self.is_online = server[Server.online]
        self.game = server[Server.game].upper()
        self.status_emoji = Emoji.UP if self.is_online else Emoji.DOWN
        self.game_emoji = Emoji.ETS2 if self.game == "ETS2" else Emoji.ATS
        self.status = online_str if self.is_online else offline_str
        self.queue = server[Server.queue] if self.is_online else queue_if_offline_str

        self.short_name = server[Server.short_name]
        self.name = server[Server.name]
        self.is_event = server[Server.event]

        self.formatted_name = self.short_name
        if self.is_event:
            self.formatted = util.trim_string(self.name)

        self.current_players = server[Server.players]
        self.max_players = server[Server.max_players]
        self.percent_players = int((self.current_players / self.max_players) * 100)
        self.players = f"{self.current_players}/{self.max_players}"
        if not self.is_online:
            self.players = players_if_offline_str

        self.speed_limiter = server[Server.speed_limiter]
        self.collisions = server[Server.collisions]
        self.cars_for_players = server[Server.cars_for_players]
        self.afk_enabled = server[Server.afk_enabled]
        self.promods = server[Server.promods]

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


class LocationAttributes:

    def __init__(self, location):
        self.server = location[Location.server]
        self.name = location[Location.name]
        self.trimmed_name = util.trim_string(self.name, 17)
        self.game = location[Location.game].upper()
        self.game_emoji = Emoji.ETS2 if self.game == "ETS2" else Emoji.ATS
        self.players = location[Location.players]

        self.severity = location[Location.severity]
        self.severity_icon = TRAFFIC_SEVERITY[self.severity][0]
        self.severity_bar = TRAFFIC_SEVERITY[self.severity][1]

        self.server_name = self.server[TrafficServer.name]
        self.server_short_name = self.server[TrafficServer.short_name]

        self.server_formatted_name = self.server_short_name
        if "event" in self.server[TrafficServer.url]:
            self.server_formatted_name = util.trim_string(self.server_name, 9)
