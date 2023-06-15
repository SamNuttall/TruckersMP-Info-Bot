import asyncio
from typing import Optional

import aiosqlite
import interactions as ipy

from common.discord import permissions
from common.ui import retrieve as ui


class Guild:
    id: int
    last_seen: Optional[str]  # None indicates the guild is still visible

    @classmethod
    def create_from_row(cls, row):
        """Create from a guilds table row in the database"""
        self = Guild()
        self.id, self.last_seen = row
        return self

    @classmethod
    def create(cls, guild_id: int, last_seen: Optional[str] = None):
        self = Guild()
        self.id, self.last_seen = guild_id, last_seen
        return self

    async def get_object(self, bot: ipy.Client):
        return await bot.fetch_guild(self.id)


class Pin:
    id: Optional[int]  # no ID indicates this pin is not in the DB or was not recieved from it
    type: int
    guild: Guild
    channel_id: int
    message_id: int

    @classmethod
    def create_from_row(cls, row):
        """
        Create from a joined row in the database.
        Expects the guilds table to be joined onto the right side of the pins table, with the guild_id from pin removed
        row: (0) [pins] id, (1) type, (2) channel_id, (3) message_id, (4) [guilds] id, (5) guild_id, (6) last_seen
        """
        self = Pin()
        self.guild = Guild.create_from_row(row[4:6])
        self.id, self.type, self.channel_id, self.message_id = row[0:4]
        return self

    @classmethod
    async def fetch(cls, conn, guild_id: int, channel_id: int, message_id: int):
        """
        Create from raw variables, fetching the object from the database
        """
        return Pin.create_from_row(await get_pin(conn, guild_id, channel_id, message_id))

    @classmethod
    async def create_and_finish(cls, bot: ipy.Client, pin_type, guild_id: int, channel_id: int):
        """
        Create from the bare minimum and then automatically send the message, get it's ID and write to the database.
        """
        self = Pin()
        self.guild = Guild.create(guild_id)
        self.type, self.channel_id = pin_type, channel_id
        await self.send_new(bot)
        await self.write_to_db(bot.db)
        return self

    async def send_new(self, bot: ipy.Client):
        """
        Send a message to Discord and assign this pin to it
        """
        sendable, channel = await asyncio.gather(
            self.get_sendable(bot),
            bot.fetch_channel(self.channel_id)
        )
        message = await channel.send(embed=sendable)
        self.message_id = message.id

    async def write_to_db(self, conn: aiosqlite.Connection):
        await add_pin(conn, self)

    async def delete_from_db(self, conn: aiosqlite.Connection):
        await delete_pin(conn, self.id)

    async def get_sendable(self, bot: ipy.Client):
        match self.type:
            case 1:
                return await ui.Servers.overview(bot)
            case 2:
                return await ui.Traffic.overview()
            case 3:
                return ipy.Embed(title="Events Soon")

    async def update(self, bot: ipy.Client) -> bool:
        sendable, channel = await asyncio.gather(
            self.get_sendable(bot),
            bot.fetch_channel(self.channel_id)
        )
        message = await channel.fetch_message(self.message_id)
        if not permissions.check_channel_permissions(bot.user, channel, permissions.SEND_AND_EDIT)[0]:
            return False
        if message is None:
            return False
        await message.edit(embed=sendable)
        return True


async def get_pins(
        conn: aiosqlite.Connection,
        guild_id: int = None,
        exclude_invisible_guilds: bool = False
) -> list[Pin]:
    """
    Get all pins from the db. Optionally filter by guild_id or exclude guilds marked as invisible
    """
    where = ""
    params = ()
    if exclude_invisible_guilds:
        where = "WHERE g.last_seen IS NULL"
    elif guild_id is not None:
        where = "WHERE g.id = ?"
        params = (guild_id,)

    query = f"""
    SELECT p.id, p.type, p.channel_id, p.message_id, g.id, g.last_seen
    FROM pins AS p INNER JOIN guilds as g ON p.guild_id = g.id {where};
    """
    pins = []
    async with conn.execute(query, params) as cursor:
        async for row in cursor:
            pins.append(Pin.create_from_row(row))
    return pins


async def get_pin(conn: aiosqlite.Connection, guild_id: int, channel_id: int, message_id: int) -> Pin:
    for pin in await get_pins(conn, guild_id=guild_id):
        if pin.message_id == message_id and pin.channel_id == channel_id:
            return pin


async def add_pin(conn: aiosqlite.Connection, pin: Pin):
    await conn.execute(
        "INSERT OR IGNORE INTO guilds (id) VALUES (?);",
        (pin.guild.id,)
    )
    await conn.execute(
        "INSERT INTO pins (type, guild_id, channel_id, message_id) VALUES (?, ?, ?, ?)",
        (pin.type, pin.guild.id, pin.channel_id, pin.message_id)
    )
    await conn.commit()


async def delete_pin(conn: aiosqlite.Connection, pin_id: int):
    await conn.execute("DELETE FROM pins WHERE id = ?;", (pin_id,))
    await conn.commit()
