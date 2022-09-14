# Core; Logic: Command

import sys

import interactions
from interactions import CommandContext

import config
from core import util, log
from core.discord import component as dc
from core.interface import base as i
from core.interface import embed
from core.public import Caches


class Public:
    @staticmethod
    async def servers(ctx: CommandContext, server: int, game: str):
        log.interaction(ctx, "servers")
        if server and game:
            game = None
        server_id = server

        embeds_func = i.Servers.singular(server_id) if server_id else i.Servers.overview(game)

        await ctx.send(
            embeds=await embeds_func,
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @staticmethod
    async def traffic(ctx, location: str, server: str, game: str):
        log.interaction(ctx, "traffic")

        if server and game:
            game = None

        await ctx.send(
            embeds=await i.Traffic.overview(location, server, game),
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @staticmethod
    async def player(ctx, player_id: int, player_name: str):
        log.interaction(ctx, "player")

        await ctx.send(
            embeds=await i.Player.singular(player_id, player_name),
            ephemeral=config.EPHEMERAL_RESPONSES
        )

    @staticmethod
    async def events(ctx, event_id: int):
        log.interaction(ctx, "events")

        if event_id:
            embeds_func = i.Events.singular(event_id)
            components = None
        else:
            embeds_func = i.Events.overview()
            components = interactions.spread_to_rows(
                dc.SelectMenu.get_event_lists(),
                await dc.SelectMenu.get_event_selector()
            )

        await ctx.send(embeds=await embeds_func,
                       ephemeral=config.EPHEMERAL_RESPONSES,
                       components=components
                       )

    @staticmethod
    async def info(ctx, conf):
        log.interaction(ctx, "info")
        await ctx.send(
            embeds=embed.bot_info(
                embed.BOT_AVATAR_URL,
                conf.BOT_INVITE_URL,
                conf.PRIVACY_POLICY_URL,
                conf.SOURCE_CODE_URL
            ),
            ephemeral=config.EPHEMERAL_RESPONSES)

    @staticmethod
    async def feedback(ctx):
        if Caches.feedback.get(ctx.author.id) is not None:
            await ctx.send("You have already sent feedback within the last 24 hours. Try again later.", ephemeral=True)
            return

        modal = dc.Modal.feedback
        await ctx.popup(modal)


class Private:
    @staticmethod
    async def devinfo(ctx, bot, owner_id):
        log.interaction(ctx, "devinfo")
        if ctx.author.user.id != owner_id:
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return
        guilds = ""
        for index, guild in enumerate(bot.guilds):
            guilds += f"[{index}] {guild.id} - {guild.name}\n"
        content = ("```"
                   f"Num of Guilds: {len(bot.guilds)}\n"
                   f"Py Version: {sys.version}\n\n"
                   f"Guilds:\n{guilds}"
                   "```"
                   )
        await ctx.send(content, ephemeral=True)

    @staticmethod
    async def cache(ctx, owner_id):
        log.interaction(ctx, "cache")
        if ctx.author.user.id != owner_id:
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return
        info = util.get_cache_info()
        await ctx.send(f":file_folder: **Caches** | Chars: {len(info)}```{util.get_cache_info()}```", ephemeral=True)
