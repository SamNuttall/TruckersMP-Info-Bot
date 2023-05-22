"""
Provides global utility functions related to startup
"""

import os

import interactions as ipy

import config
from common.const import logger


def is_configured_correctly() -> bool:
    """
    Checks if the bot is configured correctly by running checks to ensure bot is configured correctly.
    Outputs a critical log message if configured incorrectly.
    Returns true if checks passed
    """
    log_start = "Bot cannot start, check failed:"
    is_passed = True

    if "APP_TOKEN" not in os.environ:
        logger.critical(f"{log_start} Token is not specified as an environmental variable")
        is_passed = False

    if not "STEAM_KEY" not in os.environ:
        logger.critical(f"{log_start} Steam API key is not specified as an environmental variable")
        is_passed = False

    if type(config.ADMIN_GUILD_ID) is not int:
        logger.critical(f"{log_start} Admin guild id (specified in the configuration file) is not an integer")
        is_passed = False

    if (config.GUILD_ID is not None) and (config.GUILD_ID is not ipy.MISSING):
        if type(config.GUILD_ID) is not int:
            logger.critical(f"{log_start} Guild id (specified in the configuration file) is not an integer")
            is_passed = False

    if type(config.EPHEMERAL_RESPONSES) is not bool:
        logger.critical(f"{log_start} Ephemeral Responses (specified in the configuration file) is not a boolean")
        is_passed = False

    return is_passed


def load_exts(bot) -> bool:
    """
    Automatically load extensions from the exts directory.
    Will only load files ending in .py and not starting with _ (underscore)
    Returns false if any extension failed to load
    """
    ext_paths = [  # list of strings containing paths to each extension
        f"extensions.{f[:-3]}"
        for f in os.listdir("./exts")
        if f.endswith(".py") and not f.startswith("_")
    ]
    loaded_exts = []
    success = True
    for ext in ext_paths:
        try:
            bot.load_extension(ext)
            loaded_exts.append(ext)
        except ipy.errors.ExtensionLoadException as e:
            logger.exception(f"Failed to load extension: {ext}.", exc_info=e)
            success = False
    logger.info(f"Loaded {len(loaded_exts)} extension(s): {', '.join(loaded_exts)}.")
    return success


async def on_ready(bot) -> None:
    """
    Run when the bot is ready to inform the user.
    """
    ready_string = f"Ready; Logged in as {bot.me.name}"
    logger.info(ready_string + f" (ID: {bot.me.id})")
    print(ready_string)
