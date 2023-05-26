"""
Sets up constants to be used throughout the program
Creates loggers, caches, limiters, and the bot instance.
"""

import logging
from datetime import timedelta
import os

import interactions as ipy
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
from truckersmp import TruckersMP
from truckersmp.cache import Cache

import config

load_dotenv()

# Setup Logging
logger = logging.getLogger("alfie-bot")
logger.setLevel(logging.DEBUG)
# Log to file
log_fh = logging.FileHandler("./log.log")
log_fh.setLevel(logging.DEBUG)
log_fh.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(log_fh)
# Log to console
log_sh = logging.StreamHandler()
log_sh.setLevel(logging.WARNING)
logger.addHandler(log_sh)

truckersmp = TruckersMP(logger=logger)

bot = ipy.Client(
    token=os.environ["APP_TOKEN"],
    intents=ipy.Intents.DEFAULT,
    debug_scope=config.ADMIN_GUILD_ID,
    activity=ipy.Activity.create(name="TruckersMP"),
    logger=logger
)


class Caches:  # Stores all caches, uses async-truckersmp implementation
    traffic_servers = Cache(name="traffic_servers", max_size=1, time_to_live=90)  # Traffic servers stored in one obj
    traffic = Cache(name="traffic", max_size=20, time_to_live=90)  # Each traffic server is stored as a seperate obj
    time = Cache(name="time", max_size=1, time_to_live=5)
    steam_vanityurl = Cache(name="steam_vanityurl", max_size=3000, time_to_live=timedelta(days=5))
    sim_score = Cache(name="sim_score", max_size=200_000)
    server_choice = Cache(name="server_choice", max_size=2000)
    location_choice = Cache(name="location_choice", max_size=10000)
    feedback = Cache(name="feedback", time_to_live=timedelta(days=1))  # Acts as a rate limiter for feedback


class Limiters:  # Stores limiters for which API calls need to be made outside async-truckersmp
    trucky_api = AsyncLimiter(15, 20)  # 15 requests / 20 secs
    steam_api = AsyncLimiter(20, 20)  # 20 requests / 20 secs (Steam API rate limit: 100K / day)
