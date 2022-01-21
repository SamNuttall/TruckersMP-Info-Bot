from interactions import Choice
from difflib import SequenceMatcher
from cache import AsyncLRU


@AsyncLRU(maxsize=1024)
async def get_server_choices(servers: list, search: str = "", maximum: int = 25, min_sim_score: float = 0.2):
    """
    Get a list of TruckersMP servers to use as choices

    Args:
        servers: list = List of dicts containing each server's info
        search: str = Term to order list by
        maximum: int = maximum number of choices returned
        min_sim_score: float = remove servers with a lower sim score (smallest similarity to search)
    Returns:
        list: interactions.Choice
    """
    choice_list = []
    if search != "":
        for server in servers:
            server['sim_score'] = SequenceMatcher(None, server['name'], search).ratio()
            server['contains'] = 1 if search.lower() in server['name'].lower() else 0
        servers = sorted(servers, key=lambda x: (x['contains'], x['sim_score']), reverse=True)
    for server in servers:
        if len(choice_list) >= maximum or (search != "" and server['sim_score'] <= min_sim_score):
            break
        choice_list.append(Choice(
            name=f"{server['name']} ({server['game']})",
            value=server['id']
        ))
    return choice_list


def get_traffic_server_choices():
    """
    Get a list of TruckersMP traffic servers to use as choices

    Pending implementation
    """


def get_city_choices():
    """
    Get a list of in-game cities to use as choices

    Pending implementation
    """
