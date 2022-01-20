import aiohttp
import asyncio


async def get_request(url: str, headers: dict = None, timeout: int = 10):
    """
    Makes a web get request (eg. to an API) for JSON.

    Args:
        url: str = The endpoint of the get request
        headers: dict = HTTP headers to send with the request
        timeout: int = How long to wait for a response before cancelling
    Returns:
        dict =
            error: bool = True if status not 200 or not other error
            resp?: str = The json response from the endpoint
    """
    result = dict()
    result['error'] = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout) as resp:
                if resp.status == 200:
                    result['resp'] = await resp.json()
                if 'resp' not in result:
                    result['error'] = True
    except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ServerTimeoutError):
        result['error'] = True
    return result


def validate_resp(func_resp: dict, expected_keys: tuple):
    """
    Check if a get request response is valid

    Args:
        func_resp: dict = Data returned by the get_request function
        expected_keys: dict = Keys excepted to be in the json response (from endpoint)
    Returns:
        bool = True if valid
    """
    if func_resp['error']:
        return False
    if 'resp' not in func_resp:  # Should never happen
        return False
    resp = func_resp['resp']
    if expected_keys not in resp:
        return False
    return True
