# Core: Data
# Handles getting data required by the bot.

import asyncio

from datetime import datetime, timezone, timedelta
from truckersmp import exceptions
from truckersmp.base import wrapper
from core.public import logger, Caches, Limiters

TIMEOUT = 10  # secs


async def get_traffic_servers():
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


async def get_traffic(traffic_servers: list):
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


def get_ingame_time():
    """
    Gets the approximate in-game time (local, no API)

    Returns:
        datetime = The approximate in-game time (only hour & min mostly important)
    """
    def logic():
        epoch = datetime(2015, 10, 25, 15, 48, 32, tzinfo=timezone.utc)  # From TruckersMP API docs
        offset = timedelta(minutes=48, hours=15)  # This appears to align regardless of docs; Reason unknown
        time_now = datetime.now(timezone.utc)

        since_epoch = time_now - epoch
        ingame_mins_since_epoch = timedelta(
            seconds=since_epoch.total_seconds() * 6)  # 10 real sec = 60 in-game sec (x*6)
        game_time = epoch + ingame_mins_since_epoch + offset

        return game_time

    return Caches.time.execute(logic)


async def get_steamid_via_vanityurl(steam_key, vanity_url: str):
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
