"""
Run this file to start the bot.
"""

from common import startup_utils
from common.const import bot


def main():
    if not startup_utils.is_configured_correctly():
        print("Failed startup checks; Check log file for info!")
        quit(1)
    startup_utils.load_exts(bot)
    bot.start()


if __name__ == "__main__":
    main()
