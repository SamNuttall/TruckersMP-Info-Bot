"""
Stores components used throughout the bot such as menus, buttons and modals
"""

import interactions as ipy
from truckersmp import exceptions
from truckersmp.base import execute

from common import utils
from common.const import truckersmp


class Button:
    EVENT_BACK = "event-back-btn"


class SelectMenu:
    EMPTY = "empty_selectmenu"
    EVENTS = "events_selectmenu"
    EVENTS_SELECTOR = "events_selector_selectmenu"

    @staticmethod
    def _empty(message: str):
        """Create an empty SelectMenu. Should really be used for error display only."""
        return ipy.StringSelectMenu(
            ipy.StringSelectOption(
                label=message,
                value=SelectMenu.EMPTY
            ),
            custom_id=SelectMenu.EMPTY,
            placeholder=message,
        )

    @staticmethod
    def get_event_lists(default: str = "featured"):
        options = {
            'featured': {
                'label': "Featured",
                'value': "featured",
                'desc': "See events featured by TruckersMP",
                'emoji': ipy.PartialEmoji(name="⭐")
            },
            'upcoming': {
                'label': "Upcoming",
                'value': "upcoming",
                'desc': "See events which are starting soonest",
                'emoji': ipy.PartialEmoji(name="📆")
            },
            'now': {
                'label': "Now",
                'value': "now",
                'desc': "See events which are happening now",
                'emoji': ipy.PartialEmoji(name="🚚")
            }
        }

        selectmenu_options = list()
        for option in options.items():
            title = option[0]
            data = option[1]
            is_default = title == default
            selectmenu_options.append(
                ipy.StringSelectOption(
                    label=data['label'],
                    value=data['value'],
                    description=data['desc'],
                    emoji=data['emoji'],
                    default=is_default
                )
            )

        return ipy.StringSelectMenu(
            *selectmenu_options,
            custom_id=SelectMenu.EVENTS,
        )

    @staticmethod
    async def get_event_selector(list_type: str = "featured"):
        try:
            events = await execute(truckersmp.get_events)
        except exceptions.ExecuteError:
            return SelectMenu._empty("Failed to load events.")
        options = list()
        events = utils.get_list_from_events(events, list_type)
        if len(events) <= 0:
            return  # Don't display a selector if no events are given
        for event in events:
            options.append(ipy.StringSelectOption(
                label=event.name,
                description=utils.format_time(event.start_at, '%a, %d %B %Y'),
                value=f"{event.id}#{list_type}"  # Value is ID & current list type, seperated by a hash
            ))
        return ipy.StringSelectMenu(
            *options,
            custom_id=SelectMenu.EVENTS_SELECTOR,
            placeholder="Select an event for details"
        )


class Modal:
    feedback = ipy.Modal(
        ipy.ShortText(
            custom_id="subject_input",
            label="Subject (optional)",
            required=False,
            max_length=50
        ),
        ipy.ParagraphText(
            custom_id="content_input",
            label="Give feedback, bug reports or comments here!",
            required=True,
            min_length=10,
            max_length=3600  # Allow space for other information
        ),
        custom_id="feedback_form",
        title="Alfie Feedback Form"
    )
