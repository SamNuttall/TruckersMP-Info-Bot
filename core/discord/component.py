# Core; Discord: Component
# Stores and creates components used throughout the bot

import interactions
from interactions import Emoji, SelectOption
from truckersmp import exceptions
from truckersmp.base import execute

from core import util
from core.public import truckersmp


class Button:
    EVENT_BACK = "event-back-btn"


class SelectMenu:
    EMPTY = "empty_selectmenu"
    EVENTS = "events_selectmenu"
    EVENTS_SELECTOR = "events_selector_selectmenu"

    @staticmethod
    def _empty(message: str):
        """Create an empty SelectMenu. Should really be used for error display only."""
        return interactions.SelectMenu(
            custom_id=SelectMenu.EMPTY,
            placeholder=message,
            options=[
                interactions.SelectOption(
                    label=message,
                    value=SelectMenu.EMPTY
                )
            ]
        )

    @staticmethod
    def get_event_lists(default: str = "featured"):
        options = {
            'featured': {
                'label': "Featured",
                'value': "featured",
                'desc': "See events featured by TruckersMP",
                'emoji': Emoji(name="⭐")
            },
            'upcoming': {
                'label': "Upcoming",
                'value': "upcoming",
                'desc': "See events which are starting soonest",
                'emoji': Emoji(name="📆")
            },
            'now': {
                'label': "Now",
                'value': "now",
                'desc': "See events which are happening now",
                'emoji': Emoji(name="🚚")
            }
        }

        selectmenu_options = list()
        for option in options.items():
            title = option[0]
            data = option[1]
            is_default = title == default
            selectmenu_options.append(
                SelectOption(label=data['label'],
                             value=data['value'],
                             description=data['desc'],
                             emoji=data['emoji'],
                             default=is_default
                             )
            )

        return interactions.SelectMenu(
            custom_id=SelectMenu.EVENTS,
            options=selectmenu_options
        )

    @staticmethod
    async def get_event_selector(list_type: str = "featured"):
        try:
            events = await execute(truckersmp.get_events)
        except exceptions.ExecuteError:
            return SelectMenu._empty("Failed to load events.")
        options = list()
        events = util.get_list_from_events(events, list_type)
        for event in events:
            options.append(SelectOption(
                label=event.name,
                description=util.format_time(event.start_at, '%a, %d %B %Y'),
                value=event.id
            ))
        return interactions.SelectMenu(
            custom_id=SelectMenu.EVENTS_SELECTOR,
            options=options,
            placeholder="Select an event for details"
        )


class Modal:
    feedback = interactions.Modal(
        custom_id="feedback_form",
        title="Alfie Feedback Form",
        components=[
            interactions.TextInput(
                custom_id="subject_input",
                label="Subject (optional)",
                style=interactions.TextStyleType.SHORT,
                required=False,
                max_length=50
            ),
            interactions.TextInput(
                custom_id="content_input",
                label="Give feedback, bug reports or comments here!",
                style=interactions.TextStyleType.PARAGRAPH,
                required=True,
                min_length=10,
                max_length=3600  # Allow space for other information
            )
        ]
    )
