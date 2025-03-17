"""
Run this file to start the bot.
"""
import asyncio

from tortoise import Tortoise

from common import startup_utils
from common.const import bot


async def run():
    await Tortoise.init(
        db_url='sqlite://db.sqlite',
        modules={'models': ['common.data.db.models']}
    )
    await Tortoise.generate_schemas()
    try:
        await bot.astart()
    finally:
        await Tortoise.close_connections()


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
