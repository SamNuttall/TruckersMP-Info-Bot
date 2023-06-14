"""
Handles gathering of data from the web which cannot be retrieved via async-truckersmp
Uses async-truckersmp utilities for aid (often for caching)
"""

import asyncio

from datetime import datetime, timezone, timedelta
from math import floor

from truckersmp import exceptions
from truckersmp.base import wrapper

from common import utils
from common.const import logger, Caches, Limiters, truckersmp

TIMEOUT = 10  # secs


async def get_traffic_servers() -> list:
    """
    Gets a list of all TruckersMP traffic servers

    Returns:
        servers: list = List of TrafficServer
    """
    url = "https://api.truckyapp.com/v2/traffic/servers"
    key = 'traffic_servers'
    resp = await wrapper(url, Caches.traffic_servers, TIMEOUT, Limiters.trucky_api, logger, key)
    servers = list()
    try:
        for server in resp['response']:
            servers.append(server)
    except (KeyError, TypeError):
        raise exceptions.FormatError()
    else:
        return servers


async def get_traffic(traffic_servers: list) -> list:
    """
    Gets a list of all traffic in each city, on each server, sorted by players

    Args:
        traffic_servers: list = List of dicts containing server info (Warn: 1 API call per item)
    Returns:
        traffic: list = List of dicts containing traffic location data
    """
    url = "https://api.truckyapp.com/v2/traffic"
    tasks = []
    game_order = []
    for server in traffic_servers:
        game_order.append(server['game'].upper())
        params = {'game': server['game'], 'server': server['url']}
        key = str(server['url'])
        tasks.append(
            wrapper(url, Caches.traffic, TIMEOUT, Limiters.trucky_api, logger, key, params=params)
        )
    resps = await asyncio.gather(*tasks)

    traffic = []
    try:
        for index, resp in enumerate(resps):
            countries = resp['response']
            for country in countries:
                for location in country['locations']:
                    location['game'] = game_order[index]
                    location['server'] = traffic_servers[index]
                    traffic.append(location)
        traffic = sorted(traffic, key=lambda x: (x['players']), reverse=True)
    except (KeyError, TypeError):
        raise exceptions.FormatError()
    return traffic


async def sync_time():
    """
    Sync the API ingame-time for use locally.
    Returns a dictionary with the value from the API (val: int) and when it was fetched (at: int)
    Will return None if the call fails, in which case fallback values should be used.
    """
    try:
        api_time = await truckersmp.get_ingame_time()
    except exceptions.FormatError:
        return
    else:
        game_time = {
            'val': api_time,
            'at': round(datetime.utcnow().timestamp())  # unix
        }
        return game_time


def get_ingame_time(synced_time: dict = None) -> datetime:
    """
    Gets the approximate in-game time using the synced time

    Returns:
        datetime = The approximate in-game time (only hour & min)
    """
    def logic():
        game_time = synced_time
        if game_time is None:
            game_time = {'val': 24150266, 'at': 1686732595}  # fallback to tested values

        now = round(datetime.utcnow().timestamp())
        calc_time = game_time['val'] + ((now - game_time['at']) / 10)  # calc diff in time between now and last sync
        display_time = (calc_time - 2) * 60  # -2 to account for visual difference (not sure on the reason)
        hours = (display_time / 3600) % 24
        mins = (display_time / 60) % 60

        return datetime.strptime(f"{floor(hours)}:{floor(mins)}", "%H:%M")

    return Caches.time.execute(logic)


async def get_steamid_via_vanityurl(steam_key, vanity_url: str) -> str:
    """
    Gets the SteamID of a user via their vanity_url
    """
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001"
    params = {'key': steam_key, 'vanityurl': vanity_url}
    resp = await wrapper(url, Caches.steam_vanityurl,
                         TIMEOUT, Limiters.steam_api, logger, vanity_url, params=params)
    resp = resp['response']
    steam_id = None
    if resp['success'] == 1:
        steam_id = resp['steamid']
    return steam_id
