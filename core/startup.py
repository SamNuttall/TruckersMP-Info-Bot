# Core: Startup
# Handles startup of the bot.
from os import listdir

from interactions import MISSING

from core.public import logger, TOKEN, STEAM_KEY
from core.public import usr_config as config


def checks():
    """Runs pre-checks to ensure bot is configured correctly. Returns true if checks passed"""
    log_start = "Bot cannot start, check failed:"
    is_passed = True

    if not TOKEN:
        logger.critical(f"{log_start} Token is not specified as an environmental variable")
        is_passed = False

    if not STEAM_KEY:
        logger.critical(f"{log_start} Steam API key is not specified as an environmental variable")
        is_passed = False

    if type(config.ADMIN_GUILD_ID) is not int:
        logger.critical(f"{log_start} Admin guild id (specified in the configuration file) is not an integer")
        is_passed = False

    if (config.GUILD_ID is not None) and (config.GUILD_ID is not MISSING):
        if type(config.GUILD_ID) is not int:
            logger.critical(f"{log_start} Guild id (specified in the configuration file) is not an integer")
            is_passed = False

    if type(config.EPHEMERAL_RESPONSES) is not bool:
        logger.critical(f"{log_start} Ephemeral Responses (specified in the configuration file) is not a boolean")
        is_passed = False

    return is_passed


async def on_ready(bot):
    """Run when the bot is ready to inform the user."""
    ready_string = f"Ready; Logged in as {bot.me.name}"
    logger.info(ready_string + f" (ID: {bot.me.id})")
    print(ready_string)


def load_exts(bot):
    """Automatically load extensions from the core/extensions directory."""
    loaded_exts = list()
    for file_name in listdir("./core/extensions"):
        if file_name.endswith(".py") and (not file_name.startswith("_")):
            bot.load("core.extensions." + file_name[:-3])  # -3 to remove .py extension
            loaded_exts.append(file_name[:-3])
    logger.info(f"Loaded {len(loaded_exts)} extension(s): {', '.join(loaded_exts)}.")
