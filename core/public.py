# Core: Public
# Setup global classes, config and variables

import logging
from datetime import timedelta
from os import getenv

import interactions
from dotenv import load_dotenv
from interactions import MISSING, Client
from interactions.base import get_logger
from truckersmp import TruckersMP
from truckersmp.cache import Cache
from aiolimiter import AsyncLimiter

import config

# Logger Configuration
logging.basicConfig(filename="log.log",
                    level=logging.INFO,
                    format="[%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(funcName)s:%(lineno)s] %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S"
                    )

context_logger = get_logger("context")
client_logger = get_logger("client")
logger = get_logger("general")
context_logger.setLevel(logging.WARNING)
client_logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)

# Environment Variables
load_dotenv()
TOKEN = getenv("APP_TOKEN")
STEAM_KEY = getenv("STEAM_API_KEY")

# User Configuration
config.GUILD_ID = config.GUILD_ID if config.GUILD_ID else MISSING
usr_config = config

# Async-TruckersMP Library
truckersmp = TruckersMP(logger=logger)


# Cache Configuration
class Caches:
    traffic_servers = Cache(name="traffic_servers", max_size=1, time_to_live=90)  # Traffic servers stored in one obj
    traffic = Cache(name="traffic", max_size=20, time_to_live=90)  # Each traffic server is stored as a seperate obj
    time = Cache(name="time", max_size=1, time_to_live=5)
    steam_vanityurl = Cache(name="steam_vanityurl", max_size=3000, time_to_live=timedelta(days=5))
    sim_score = Cache(name="sim_score", max_size=200_000)
    server_choice = Cache(name="server_choice", max_size=2000)
    location_choice = Cache(name="location_choice", max_size=10000)
    feedback = Cache(name="feedback", time_to_live=timedelta(days=1))  # Acts as a rate limiter for feedback


# Limiter Configuration
class Limiters:
    trucky_api = AsyncLimiter(15, 20)  # 15 requests / 20 secs
    steam_api = AsyncLimiter(20, 20)  # 20 requests / 20 secs (Steam API rate limit: 100K / day)


# Bot Configuration
bot = Client(token=TOKEN,
             intents=interactions.Intents.GUILD_INTEGRATIONS,
             presence=interactions.ClientPresence(
                 activities=[interactions.PresenceActivity(
                     name="TruckersMP Stats",
                     type=interactions.PresenceActivityType.WATCHING)
                 ]
             ))
