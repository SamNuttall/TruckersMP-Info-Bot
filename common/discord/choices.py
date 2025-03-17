"""
Handles choices which are part of an option in a command.
Functions here often return a list of choices to be presented to the user.
"""
# TODO: Look into reducing memory footprint of sim_score cache and it's viability.
# Once values are cached, the time to add sim scores is reduced (~60% decrease).
# Memory footprint of current implementation is very large though. Approx at sizes:
# 52MB per 100k (520MB at 1M, 2.6GB at 5M - Original Maximum)

from difflib import SequenceMatcher

import asyncio
import interactions as ipy
from thefuzz import fuzz

from common.const import Caches
from common import utils
from common.data.db import models
from common.data.db.models import Pin


def add_sim_score_new(dict_list: list, search: str, key: str):
    def get_score(v, sh):
        v = v.lower()
        sh = sh.lower()
        s = 0
        s += fuzz.token_sort_ratio(v.split('(')[0], sh) * 3  # Partial string: "city" | Weight: 0 - 300
        s += 100 if len(sh) > 4 and sh in v else 0  # Value contains search | Weight: 0 or 100
        s += 200 if v.startswith(sh) else 0  # Value starts with search | Weight: 0 or 200
        return int((s / 600) * 100)  # max score: 500, brings score to 0 - 100

    for dictionary in dict_list:
        dictionary['sim_score'] = Caches.sim_score.execute(get_score, None, dictionary[key], search)

    return sorted(
        dict_list, key=lambda x: (x['sim_score']),
        reverse=True
    )


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


async def get_servers(servers: list, search: str = "", maximum: int = 25, min_sim_score: int = 35):
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
            s = add_sim_score_new(s, search, 'name')
        for server in s:
            valid_score = True
            if search != "":
                valid_score = server['sim_score'] >= min_sim_score
            if len(choice_list) >= maximum or not valid_score:
                break
            identifier = 'id'
            if 'id' not in server:
                identifier = 'url'
            choice_list.append(ipy.SlashCommandChoice(
                name=f"{server['name']} ({server['game'].upper()})",
                value=server[identifier]
            ))
        return choice_list

    servers = to_dicts()
    server_names = utils.strip_dict_key_value(servers, "name")
    key = (tuple(server_names), search, maximum, min_sim_score)
    return Caches.server_choice.execute(logic, key)


async def get_locations(locations: list, search: str = "", maximum: int = 25, min_sim_score: int = 35):
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
            locs = add_sim_score_new(locs, search, 'name')
        for location in locs:
            valid_score = True
            if search != "":
                valid_score = location['sim_score'] >= min_sim_score
            if not valid_score:
                continue
            if len(choice_list) >= maximum:
                break
            if location['name'] not in added_locations:
                choice_list.append(ipy.SlashCommandChoice(
                    name=f"{location['name']} ({location['country']}) ({location['game']})",
                    value=location['name']
                ))
                added_locations.append(location['name'])
        return choice_list

    location_names = utils.strip_dict_key_value(locations, "name")
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
        choice_list.append(ipy.SlashCommandChoice(
            name=f"{full_name} ({short_name})",
            value=short_name
        ))
    return choice_list


def get_pin_types():
    choice_list = []
    for type_id, name in models.PIN_TYPE_NAMES.items():
        choice_list.append(ipy.SlashCommandChoice(
            name=name,
            value=type_id
        ))
    return choice_list


async def get_guild_pins(bot: ipy.Client, guild_id: int, filter_text: str = ""):
    pins = await Pin.filter(guild_id=guild_id).all()

    async def get_command_choice(p: Pin):
        channel_name = "unknown"
        channel = await bot.fetch_channel(p.channel_id)
        if channel is not None:
            channel_name = channel.name
        display_name = f"{p.type_name} in #{channel_name}"
        if filter_text.lower() not in display_name.lower():
            return None
        return ipy.SlashCommandChoice(
            name=display_name,
            value=p.id
        )

    tasks = [get_command_choice(pin) for pin in pins]
    choice_list = await asyncio.gather(*tasks)
    return filter(None, choice_list)
