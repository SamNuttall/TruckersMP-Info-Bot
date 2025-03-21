"""
Combines data and interface components by acting as a controller/middleperson
In the end, most methods should return a message sendable (like an embed)
"""
import os

from truckersmp import exceptions
from truckersmp.base import execute

from common import utils
from common.ui import embeds
from common.const import truckersmp
from common.data import retrieve as data


class Servers:
    @staticmethod
    async def _get_base_data(bot):
        servers = await execute(truckersmp.get_servers)
        ingame_time = utils.format_time(data.get_ingame_time(bot.synced_ingame_time))
        return servers, ingame_time

    @staticmethod
    async def overview(bot, game: str = None):
        try:
            servers, ingame_time = await Servers._get_base_data(bot)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        return embeds.servers_stats(
            servers=servers,
            filter_by_game=game,
            ingame_time=ingame_time
        )

    @staticmethod
    async def singular(bot, server_id: int):
        try:
            servers, ingame_time = await Servers._get_base_data(bot)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        server = utils.get_server_via_id(servers, server_id)
        if server is None:
            return embeds.item_not_found("Specified TruckersMP server")
        return embeds.server_stats(
            server=server,
            ingame_time=ingame_time
        )


class Traffic:
    @staticmethod
    async def overview(location: str = None, server: str = None, game: str = None):
        try:
            servers = await execute(data.get_traffic_servers)
            traffic = await execute(data.get_traffic, servers)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        if location:
            if not any(i['name'] == location for i in traffic):
                return embeds.item_not_found("Location")
        if server:
            if not any(i['url'] == server for i in servers):
                return embeds.item_not_found("Server")
        return embeds.traffic_stats(
            locations=traffic,
            filter_by_location=location,
            filter_by_server_data=[server, [i['name'] for i in servers if i['url'] == server][0]]
            if server else [None, None],
            filter_by_game=game
        )

    @staticmethod
    async def singular():
        return  # Stats for a single traffic location (on a single server) is not needed at this time.


class Player:
    @staticmethod
    async def overview():
        return  # A player overview is not needed at this time.

    @staticmethod
    async def singular(player_id: int = None, player_name: str = None):
        if not player_id and not player_name:
            return embeds.generic_embed("Provide a player ID or name")

        search_bad_str = "> *[Why is player search bad?]" \
                         "(https://gist.github.com/SamNuttall/2530ac8ceccf2f93a8528eff2f820404)*"

        # Steam Vanity URL Search
        if player_name:
            try:
                steam_id = await execute(data.get_steamid_via_vanityurl, os.environ["STEAM_API_KEY"], player_name)
            except exceptions.ExecuteError:
                return embeds.generic_error()
            if steam_id is None:
                desc = f"Steam user not found with that Vanity URL\n{search_bad_str}"
                return embeds.item_not_found_detailed("Player", desc)
            player_id = steam_id

        # Search for player via provided ID or Steam vanityurl result
        try:
            player = await execute(truckersmp.get_player, player_id)
        except exceptions.NotFoundError:
            desc = None
            if player_name:
                desc = f"A Steam [user](https://steamcommunity.com/profiles/{player_id}) was, but they are " \
                       f"not a TruckersMP player\n{search_bad_str}"
            return embeds.item_not_found_detailed("Player", desc)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        return embeds.player_stats(player)


class Events:
    @staticmethod
    async def overview(list_type: str = "featured", num_of_events: int = 3, include_links: bool = False):
        try:
            events = await execute(truckersmp.get_events)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        match list_type:
            case "featured":
                list_name = "Featured Events"
            case "upcoming":
                list_name = "Upcoming Events"
            case _:
                list_name = "Events on Now"
        events = utils.get_list_from_events(events, list_type)
        return embeds.events_stats(
            events=events,
            list_name=list_name,
            max_size=num_of_events,
            include_links=include_links
        )

    @staticmethod
    async def singular(event_id):
        try:
            event = await execute(truckersmp.get_event, event_id)
        except exceptions.ExecuteError:
            return embeds.generic_error()
        except exceptions.NotFoundError:
            return embeds.item_not_found("Event")

        # Add an avatar to the embed. Prioritise the VTC logo if applicable.
        async def get_avatar(is_vtc):
            if is_vtc:
                return (await execute(truckersmp.get_vtc, event.vtc.id)).logo
            return (await execute(truckersmp.get_player, event.user.id)).avatar

        try:
            avatar = await get_avatar(event.vtc.id != 0)
        except (exceptions.ExecuteError, exceptions.NotFoundError):
            return embeds.generic_error()  # If the player/vtc is not found, something has gone wrong.

        return embeds.event_stats(
            event=event,
            avatar=avatar
        )
