import asyncio
from datetime import timedelta
from enum import IntEnum, Enum
from typing import Optional

import interactions as ipy
import tortoise.timezone
from tortoise import fields, Model

from common.const import bot
from common.discord import permissions
from common.ui import retrieve as ui


class Guild(Model):
    id = fields.IntField(pk=True)
    last_seen = fields.DatetimeField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    async def guild(self):
        return await bot.fetch_guild(self.id)

    @property
    def since_seen(self):
        if self.last_seen is None:
            return timedelta(seconds=0)
        return tortoise.timezone.now() - self.last_seen

    async def mark_not_seen(self):
        if self.last_seen is None:
            self.last_seen = tortoise.timezone.now()
            await self.update_from_dict({'last_seen': self.last_seen})
            await self.save()


class PinType(IntEnum):
    SERVERS_OVERVIEW = 1
    TRAFFIC_BUSIEST = 2
    EVENTS_FEATURED = 3
    EVENTS_UPCOMING = 4
    EVENTS_NOW = 5


PIN_TYPE_NAMES = {
    1: "Servers (Overview)",
    2: "Traffic (Busiest Areas)",
    3: "Events (Featured)",
    4: "Events (Upcoming)",
    5: "Events (Now)"
}


class Pin(Model):
    id = fields.IntField(pk=True)
    type = fields.IntEnumField(PinType)
    guild = fields.ForeignKeyField('models.Guild', related_name='guilds')
    channel_id = fields.IntField()
    message_id = fields.IntField()
    last_failure = fields.DatetimeField(null=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    async def _get_sendable(cls, pin_type: int):
        """Get a sendable message"""
        num_of_events = 4
        match pin_type:
            case 1:
                return await ui.Servers.overview(bot)
            case 2:
                return await ui.Traffic.overview()
            case 3:
                return await ui.Events.overview("featured", num_of_events, True)
            case 4:
                return await ui.Events.overview("upcoming", num_of_events, True)
            case 5:
                return await ui.Events.overview("now", num_of_events, True)

    @classmethod
    async def _send_new(cls, pin_type: int, channel_id: int):
        """
        Send a message to Discord and get a pin ID

        Uses the channel_id to find the channel and uses the type to get the relevant message and send it.
        """
        sendable, channel = await asyncio.gather(
            Pin._get_sendable(pin_type),
            bot.fetch_channel(channel_id)
        )
        return await channel.send(embed=sendable)

    @classmethod
    async def create_new_msg(cls, pin_type: int, guild_id: int, channel_id: int):
        """
        Create a pin without knowing the message ID.
        Will get one by sending a new message in the specified channel
        """
        guild, message = await asyncio.gather(
            Guild.get_or_create(id=guild_id),
            Pin._send_new(pin_type, channel_id)
        )
        guild = guild[0]
        return await Pin.create(type=pin_type, guild=guild, channel_id=channel_id, message_id=message.id)

    @classmethod
    def get_expiry(cls, pin_type: int):
        ref = {
            1: timedelta(minutes=60),
            2: timedelta(minutes=60),
            3: timedelta(hours=3),
            4: timedelta(hours=3),
            5: timedelta(hours=3),
        }
        return ref.get(pin_type, timedelta(hours=24))

    @property
    def type_name(self):
        return PIN_TYPE_NAMES.get(self.type, "Unknown Type")

    @property
    def last_failed(self):
        if self.last_failure is None:
            return timedelta(seconds=0)
        return tortoise.timezone.now() - self.last_failure

    async def mark_success(self):
        if self.last_failure is not None:
            self.last_failure = None
            await self.update_from_dict({'last_failure': None})
            await self.save()

    async def mark_failed(self):
        if self.last_failure is None:
            self.last_failure = tortoise.timezone.now()
            await self.update_from_dict({'last_failure': self.last_failure})
            await self.save()

    async def _run_update(self) -> tuple[bool, Optional[str]]:
        if await self.guild.guild is None:
            await self.guild.mark_not_seen()
            return False, "the pin's parent guild cannot be found"
        sendable, channel = await asyncio.gather(
            self._get_sendable(self.type),
            bot.fetch_channel(self.channel_id)
        )
        if channel is None:
            return False, "the messages's channel cannot be found"
        if not permissions.check_channel_permissions(bot.user, channel, permissions.SEND_AND_EDIT)[0]:
            return False, "bot does not have permission to find/edit message"
        message = await channel.fetch_message(self.message_id)
        if message is None:
            return False, "the message cannot be found via it's ID"
        await message.edit(embed=sendable)
        return True, None

    async def run_update(self) -> tuple[bool, Optional[str]]:
        results = await self._run_update()
        if results[0]:
            await self.mark_success()
        else:
            await self.mark_failed()
        if self.last_failed > self.get_expiry(self.type):
            await self.delete()
        return results
