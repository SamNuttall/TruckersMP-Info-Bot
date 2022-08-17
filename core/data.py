import asyncio
import logging

from core.web import get_request, validate_resp
from cache import AsyncTTL, AsyncLRU
from datetime import datetime, timezone, timedelta
from interactions.base import get_logger
from truckersmp.cache import Cache
from core.util import strip_dict_key_value

logger = get_logger("general")

traffic_servers_cache = Cache(name="traffic_servers", max_size=1, time_to_live=90)
traffic_cache = Cache(name="traffic", max_size=1, time_to_live=90)
time_cache = Cache(name="time", max_size=1, time_to_live=5)
api_time_cache = Cache(name="api_time", max_size=1, time_to_live=120)
steam_vanityurl_cache = Cache(name="steam_vanityurl", max_size=3000, time_to_live=timedelta(days=5))


@AsyncTTL(time_to_live=60, maxsize=1)
async def get_servers():
    """
    Gets a list of all TruckersMP servers

    Returns:
        dict =
            error: bool = True if status not 200 or other error
            servers?: list = Contains dicts with server info (https://stats.truckersmp.com/api#servers_list)
    """
    logger.warning("get_servers should no longer be used. Use async-truckersmp library instead")
    # TODO: Stop using function, then remove it
    result = dict()
    result['error'] = False
    endpoint = "https://api.truckersmp.com/v2/servers"
    func_resp = await get_request(endpoint)
    if not validate_resp(func_resp, ('error', 'response')):
        result['error'] = True
        return result
    resp = func_resp['resp']
    if resp['error'] == "true":
        result['error'] = True
        return result
    result['servers'] = resp['response']
    return result


async def get_traffic_servers():
    """
    Gets a list of all TruckersMP traffic servers

    Returns:
        dict =
            error: bool = True if status not 200 or other error
            servers?: list = Contains dicts with server info
                            (https://api.truckyapp.com/docs/#api-Traffic-GetV2TrafficServers)
    """
    async def logic():
        result = dict()
        result['error'] = False
        endpoint = "https://api.truckyapp.com/v2/traffic/servers"
        func_resp = await get_request(endpoint)
        if not validate_resp(func_resp, ('response',)):
            result['error'] = True
            return result
        resp = func_resp['resp']
        result['servers'] = resp['response']
        return result

    return await traffic_servers_cache.execute_async(logic)


async def get_traffic(traffic_servers: list):
    """
    Gets a list of all traffic in each city, on each server, sorted by players

    Args:
        traffic_servers: list = List of dicts containing server info (Warn: 1 API call per item)
    Returns:
        dict =
            error: bool = True if status not 200 or not other error
            traffic?: list = List of dicts containing traffic location data
    """
    async def logic():
        result = dict()
        result['error'] = False
        endpoint = "https://api.truckyapp.com/v2/traffic"
        tasks = []
        game_order = []
        for server in traffic_servers:
            game_order.append(server['game'].upper())
            tasks.append(get_request(endpoint, params={'game': server['game'], 'server': server['url']}))
        func_responses = await asyncio.gather(*tasks)
        traffic = []
        for index, func_resp in enumerate(func_responses):
            if not validate_resp(func_resp, ('response',)):
                result['error'] = True
                return result
            resp = func_resp['resp']
            countries = resp['response']
            for country in countries:
                for location in country['locations']:
                    location['game'] = game_order[index]
                    location['server'] = traffic_servers[index]
                    traffic.append(location)
        traffic = sorted(traffic, key=lambda x: (x['players']), reverse=True)
        result['traffic'] = traffic
        return result

    return await traffic_cache.execute_async(logic)


async def get_ingame_time():
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
        ingame_mins_since_epoch = timedelta(seconds=since_epoch.total_seconds() * 6)  # 10 real sec = 60 in-game sec (x*6)
        game_time = epoch + ingame_mins_since_epoch + offset

        return game_time

    return time_cache.execute(logic)


async def get_ingame_time_from_api():
    """
    Gets the in-game time from TruckyApp API

    Returns:
        dict =
            error: bool = True if status not 200 or other error
            result?: datetime = The approximate in-game time
    """
    async def logic():
        logger.debug("Got in-game time from TruckyApp API. Local implementation is recommended.")
        result = dict()
        result['error'] = False
        endpoint = "https://api.truckyapp.com/v2/truckersmp/time"
        func_resp = await get_request(endpoint)
        if not validate_resp(func_resp, ('response',)):
            result['error'] = True
            return result
        resp = func_resp['resp']
        result['time'] = resp['response']['calculated_game_time']
        return result

    return await api_time_cache.execute_async(logic)


async def get_steamid_via_vanityurl(steam_key, vanity_url: str):
    """
    Gets the SteamID of a user via their vanity_url
    """
    async def logic():
        result = dict()
        result['error'] = False
        result['steam_id'] = None
        endpoint = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001"
        params = {'key': steam_key, 'vanityurl': vanity_url}
        func_resp = await get_request(endpoint, params=params)
        if not validate_resp(func_resp, ('response',)):
            result['error'] = True
            return result
        resp = func_resp['resp']['response']
        if resp['success'] == 1:
            result['steam_id'] = resp['steamid']
        return result

    return await steam_vanityurl_cache.execute_async(logic, vanity_url)
