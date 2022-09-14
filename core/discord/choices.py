# Core; Discord: Choices
# Handles choices which are part of an option in a command.
# Functions here often return a list of choices to be presented to the user.

# TODO: Look into reducing memory footprint of sim_score cache and it's viability.
# Once values are cached, the time to add sim scores is reduced (~60% decrease).
# Memory footprint of current implementation is very large though. Approx at sizes:
# 52MB per 100k (520MB at 1M, 2.6GB at 5M - Original Maximum)

from difflib import SequenceMatcher

from interactions import Choice

from core.public import Caches
from core.util import strip_dict_key_value


def add_sim_score(list_of_dict: list, search: str, key: str):
    """
    Adds a similarity score key + value to dictionaries in a list based on a search string
    The search string is matched against the inputted key value per dictionary.

    Args:
        list_of_dict: list = list of dicts containing key
        search: str = value to compare key with
        key: str = value to compare search to
    Returns:
        list: modified list of dictionaries new keys:
            - sim_score: entire string *
            - first_sim_score: first word *
            - trim_sim_score: any text before an open bracket "(" *
            - contains: 1 if the search string is contained within the value
            * similarity marked by float between 0 & 1 (1 being most similar)
    """

    def get_ratio(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_score(a, b):
        return Caches.sim_score.execute(get_ratio, None, a, b)

    for dictionary in list_of_dict:
        dictionary['sim_score'] = get_score(dictionary[key], search)
        dictionary['first_sim_score'] = get_score(dictionary[key].split()[0], search)
        dictionary['trim_sim_score'] = get_score(dictionary[key].split('(')[0], search)
        dictionary['contains'] = 1 if search.lower() in dictionary[key].lower() else 0

    return sorted(
        list_of_dict, key=lambda x: (x['contains'], x['sim_score'], x['trim_sim_score'], x['first_sim_score']),
        reverse=True
    )


async def get_servers(servers: list, search: str = "", maximum: int = 25, min_sim_score: float = 0.4):
    """
    Get a list of TruckersMP (traffic) servers to use as choices

    Args:
        servers: list = List of dicts or Server (will be converted to dict) containing each server's info
        search: str = Term to order list by
        maximum: int = maximum number of choices returned
        min_sim_score: float = remove servers with a lower sim score (smallest similarity to search)
    Returns:
        list: interactions.Choice
    """

    def to_dicts():
        if type(servers[0]) == dict:  # Assumption: If first item is a dict, all are
            return servers

        servers_as_dicts = list()
        for serv in servers:
            servers_as_dicts.append({'name': serv.name, 'game': serv.game, 'id': serv.id})
        return servers_as_dicts  # We only need these key-values here ^

    def logic():
        choice_list = []
        s = servers
        if search != "":
            s = add_sim_score(s, search, 'name')
        for server in s:
            valid_score = True
            if search != "":
                valid_score = max(server['sim_score'],
                                  server['trim_sim_score'],
                                  server['first_sim_score']) >= min_sim_score or server['contains'] == 1
            if len(choice_list) >= maximum or not valid_score:
                break
            identifier = 'id'
            if 'id' not in server:
                identifier = 'url'
            choice_list.append(Choice(
                name=f"{server['name']} ({server['game'].upper()})",
                value=server[identifier]
            ))
        return choice_list

    servers = to_dicts()
    server_names = strip_dict_key_value(servers, "name")
    key = (tuple(server_names), search, maximum, min_sim_score)
    return Caches.server_choice.execute(logic, key)


async def get_locations(locations: list, search: str = "", maximum: int = 25, min_sim_score: float = 0.55):
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

    def logic():
        choice_list = []
        added_locations = []
        locs = locations
        if search != "":
            locs = add_sim_score(locs, search, 'name')
        for location in locs:
            valid_score = True
            if search != "":
                valid_score = max(location['sim_score'],
                                  location['trim_sim_score'],
                                  location['first_sim_score']) >= min_sim_score or (
                                      location['contains'] == 1 or location['country'].lower() in search.lower()
                              )
            if not valid_score:
                continue
            if len(choice_list) >= maximum:
                break
            if location['name'] not in added_locations:
                choice_list.append(Choice(
                    name=f"{location['name']} ({location['country']}) ({location['game']})",
                    value=location['name']
                ))
                added_locations.append(location['name'])
        return choice_list

    location_names = strip_dict_key_value(locations, "name")
    key = (tuple(location_names), search, maximum, min_sim_score)
    return Caches.location_choice.execute(logic, key)


def get_games():
    """
    Gets the list of available games (hard-coded)

    Returns:
        list: interactions.Choice
    """
    choice_list = []
    games = {
        'ETS2': "Euro Truck Simulator 2",
        'ATS': "American Truck Simulator"
    }
    for short_name, full_name in games.items():
        choice_list.append(Choice(
            name=f"{full_name} ({short_name})",
            value=short_name
        ))
    return choice_list
