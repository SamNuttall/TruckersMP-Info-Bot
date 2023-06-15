"""
Run this file to start the bot.
"""
import asyncio

import aiosqlite

from common import startup_utils, utils
from common.const import bot


async def run():
    bot.db = await aiosqlite.connect("db.sqlite")
    try:
        await utils.execute_sql_script_from_file(bot.db, "setup.sql")
        await bot.astart()
    finally:
        await bot.db.close()


def main():
    if not startup_utils.is_configured_correctly():
        print("Failed startup checks; Check log file for info!")
        quit(1)
    startup_utils.load_exts(bot)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Exiting")


if __name__ == "__main__":
    main()
