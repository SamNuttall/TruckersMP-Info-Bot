from interactions import Choice
from difflib import SequenceMatcher
from cache import AsyncLRU


async def add_sim_score(list_of_dict: list, search: str, key: str):
    """
    Adds a similarity score to dictionaries in a list based on search

    Args:
        list_of_dict: list = list of dicts containing key
        search: str = value to compare key with
        key: str = value to compare search to
    Returns:
        list: modified list of dictionaries
    """
    for dictionary in list_of_dict:
        dictionary['sim_score'] = SequenceMatcher(None, dictionary[key], search).ratio()
        dictionary['contains'] = 1 if search.lower() in dictionary[key].lower() else 0
    return sorted(list_of_dict, key=lambda x: (x['contains'], x['sim_score']), reverse=True)


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
        servers = await add_sim_score(servers, search, 'name')
    for server in servers:
        valid_score = True
        if search != "":
            valid_score = server['sim_score'] <= min_sim_score or server['contains'] == 1
        if len(choice_list) >= maximum or not valid_score:
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


@AsyncLRU(maxsize=1024)
async def get_location_choices(locations: list, search: str = "", maximum: int = 25, min_sim_score: float = 0.2):
    """
    Get a list of in-game locations to use as choices

    Args:
        locations: list = List of dicts containing each locations' info
        search: str = Term to order list by
        maximum: int = maximum number of choices returned
        min_sim_score: float = remove servers with a lower sim score (smallest similarity to search)
    Returns:
        list: interactions.Choice
    """
    choice_list = []
    added_locations = []
    if search != "":
        locations = await add_sim_score(locations, search, 'name')
    for location in locations:
        valid_score = True
        if search != "":
            valid_score = location['sim_score'] <= min_sim_score or location['contains'] == 1
        if len(choice_list) >= maximum or not valid_score:
            break
        if location['name'] not in added_locations:
            choice_list.append(Choice(
                name=f"{location['name']} ({location['country']}) ({location['game']})",
                value=location['layerID']
            ))
            added_locations.append(location['name'])
    return choice_list
