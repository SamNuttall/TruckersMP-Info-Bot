import aiohttp
import asyncio
from interactions.base import get_logger

logger = get_logger("general")


async def get_request(url: str, headers: dict = None, params: dict = None, timeout: int = 10):
    """
    Makes a web get request (eg. to an API) for JSON.

    Args:
        url: str = The endpoint of the get request
        headers: dict = HTTP headers to send with the request
        params: dict = Parameters to pass with request
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
            async with session.get(url, headers=headers, params=params, timeout=timeout) as resp:
                logger.debug(f"GET Request: {url} = {resp.status}")
                if resp.status == 200:
                    result['resp'] = await resp.json()
                if 'resp' not in result:
                    logger.warning(f"Get request not status 200. Having to return error")
                    result['error'] = True
    except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ServerTimeoutError) as e:
        logger.warning(f"Unavoidably (probably) failed to make get request: {e}")
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
        logger.warning("'resp' keyword not in dict when validating response. Function likely called using wrong params")
        return False
    resp = func_resp['resp']
    for key in expected_keys:
        if key not in resp:
            logger.debug(f"'{key}' not found in response")
            return False
    return True
