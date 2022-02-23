from interactions.base import get_logger

logger = get_logger("general")


def checks(
        token: str
):
    """Runs pre-checks to ensure bot is configured correctly. Returns true if checks passed"""
    is_passed = True
    if not token:
        logger.critical("Bot unable to start as token is not specified as an environmental variable")
        is_passed = False

    return is_passed
