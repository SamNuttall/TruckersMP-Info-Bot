import asyncio
from core.web import get_request, validate_resp
from cache import AsyncTTL, AsyncLRU


@AsyncTTL(time_to_live=60, maxsize=1)
async def get_servers():
    """
    Gets a list of all TruckersMP servers

    Returns:
        dict =
            error: bool = True if status not 200 or other error
            servers?: list = Contains dicts with server info (https://stats.truckersmp.com/api#servers_list)
    """
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


async def get_ingame_time():
    """
    Gets the in-game time

    Pending implementation
    """
    endpoint = "https://api.truckersmp.com/v2/game_time"  # Investigate implementation without TruckyApp
    return


@AsyncTTL(time_to_live=60, maxsize=1)
async def get_traffic_servers():
    """
    Gets a list of all TruckersMP traffic servers

    Returns:
        dict =
            error: bool = True if status not 200 or other error
            servers?: list = Contains dicts with server info
                            (https://api.truckyapp.com/docs/#api-Traffic-GetV2TrafficServers)
    """
    result = dict()
    result['error'] = False
    endpoint = "https://api.truckyapp.com/v2/traffic/servers"
    func_resp = await get_request(endpoint)
    if not validate_resp(func_resp, ('response', )):
        result['error'] = True
        return result
    resp = func_resp['resp']
    result['servers'] = resp['response']
    return result


@AsyncLRU(maxsize=1)
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
        if not validate_resp(func_resp, ('response', )):
            result['error'] = True
            return result
        resp = func_resp['resp']
        countries = resp['response']
        for country in countries:
            for location in country['locations']:
                location['game'] = game_order[index]
                traffic.append(location)
    traffic = sorted(traffic, key=lambda x: (x['players']), reverse=True)
    result['traffic'] = traffic
    return result

