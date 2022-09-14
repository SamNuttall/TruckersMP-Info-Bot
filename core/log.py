# Core: Log
# Provides helpful utilities for logging

from core.public import logger


def interaction(ctx, name, is_cmd: bool = True):
    """Log an interaction with the bot"""
    req_type = "Command" if is_cmd else "Autocomplete"
    guild = ctx.guild_id if ctx.guild_id else "N/A (Direct Msg)"
    author = ctx.author.user.id if ctx.author else "Unknown"
    logger.debug(f"Handle {req_type} Request: {name} | guild: {guild} & user: {author}")
