import interactions as ipy
from interactions import Permissions

SEND_AND_EDIT = (
    Permissions.VIEW_CHANNEL,
    Permissions.SEND_MESSAGES,
    Permissions.READ_MESSAGE_HISTORY,
)


def check_channel_permissions(user: ipy.User, channel: ipy.GuildChannel, permissions: tuple):
    """
    Check if a user has permissions within a channel.
    Returns a tuple with (bool, missing_permission)
    """
    channel_perms = channel.permissions_for(user)
    for permission in permissions:
        if permission not in channel_perms:
            return False, permission
    return True, None


def get_name(perm: ipy.Permissions):
    return perm.name.title().replace("_", " ")
