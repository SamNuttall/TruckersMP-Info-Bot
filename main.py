# Main
# Run this file to start the bot.

from core.public import bot, PERSISTENCE_KEY
from core import startup


def main():
    if not startup.checks():
        print("Failed startup checks; Check log file (log.log) for info")
        quit(1)
    bot.load("interactions.ext.persistence", cipher_key=PERSISTENCE_KEY)
    startup.load_exts(bot)
    bot.start()


if __name__ == "__main__":
    main()
