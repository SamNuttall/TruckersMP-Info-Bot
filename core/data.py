from web import get_request, validate_resp


async def get_servers():
    """
    Gets a list of all TruckersMP servers

    Returns:
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


async def get_traffic_servers():
    """
    Gets a list of all TruckersMP traffic servers

    Pending implementation
    """
    endpoint = "https://api.truckyapp.com/v2/traffic/servers"
    return


async def get_traffic():
    """
    Gets a list of all traffic in each city, on each server, sorted by players

    Pending implementation
    """
    endpoint = "https://api.truckyapp.com/v2/traffic"
    return

