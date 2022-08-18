from interactions.base import get_logger

logger = get_logger("general")


def checks(
        token: str,
        steam_api_key: str,
        guild_id,
        admin_guild_id,
        ephemeral_resps
):
    """Runs pre-checks to ensure bot is configured correctly. Returns true if checks passed"""
    log_start = "Bot cannot start, check failed:"
    is_passed = True

    if not token:
        logger.critical(f"{log_start} Token is not specified as an environmental variable")
        is_passed = False

    if not steam_api_key:
        logger.critical(f"{log_start} Steam API key is not specified as an environmental variable")
        is_passed = False

    if type(admin_guild_id) is not int:
        logger.critical(f"{log_start} Admin guild id (specified in the configuration file) is not an integer")
        is_passed = False

    if guild_id is not None:
        if type(guild_id) is not int:
            logger.critical(f"{log_start} Guild id (specified in the configuration file) is not an integer")
            is_passed = False

    if type(ephemeral_resps) is not bool:
        logger.critical(f"{log_start} Ephemeral Responses (specified in the configuration file) is not a boolean")
        is_passed = False

    return is_passed
