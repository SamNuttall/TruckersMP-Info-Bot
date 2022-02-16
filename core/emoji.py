from enum import Enum

USE_EXCLUSIVE = True


class Emoji(Enum):
    """Stores emoji as strings in the format <:name:id>"""
    UP = "<:Server_Online:856556236137037835>"
    DOWN = "<:Server_Offline:856560729033539594>"
    ETS2 = "<:ETS2_Server:856571359764283393>"
    ATS = "<:ATS_Server:856571360163921930>"
    PM = "<:Promods_Enabled:856546250975608883>"
    SL_ON = "<:Speed_Limiter_Enabled:856556236501024778>"
    SL_OFF = "<:Speed_Limiter_Disabled:856542645525938177>"
    CO_ON = "<:Collisions_Enabled:856556236538904596>"
    CO_OFF = "<:Collisions_Disabled:856543845542133800>"
    CA_ON = "<:Cars_Allowed:856556235994038293>"
    CA_OFF = "<:Cars_Disallowed:856548932712267786>"
    AFK_ON = "<:AFK_Kick_Enabled:856556236165742634>"
    AFK_OFF = "<:AFK_Kick_Disabled:856544424967143424>"
    T_DEF = "<:truck_gray:856974918414499890>"
    T_LOW = "<:Low_Traffic:856975295218581534>"
    T_MOD = "<:Moderate_Traffic:856986443637063690>"
    T_CON = "<:Congested_Traffic:856986443619631175>"
    T_HEV = "<:Heavy_Traffic:856988618340958208>"


def get(emoji: Emoji):
    """Gets the raw value of an emoji"""
    return emoji.value


def as_dict(emoji: Emoji):
    """Converts an Emoji into a dictionary"""
    name, emoji_id = get(emoji)[2:-1].split(":")
    return {'name': name, 'id': emoji_id}


TRAFFIC_SEVERITY = {
    'Empty': f"{get(Emoji.T_DEF)} " * 4,
    'Fluid': f"{get(Emoji.T_LOW)} " + f"{get(Emoji.T_DEF)}" * 3,
    'Moderate': f"{get(Emoji.T_LOW)} {get(Emoji.T_MOD)} " + f"{get(Emoji.T_DEF)}" * 2,
    'Congested': f"{get(Emoji.T_LOW)} {get(Emoji.T_MOD)} {get(Emoji.T_CON)} {get(Emoji.T_DEF)}",
    'Heavy': f"{get(Emoji.T_LOW)} {get(Emoji.T_MOD)} {get(Emoji.T_CON)} {get(Emoji.T_HEV)}"
}

