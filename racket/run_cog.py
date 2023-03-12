"""Utility for running a cog. See run_cog docstring for more details."""
from collections.abc import Sequence
import logging
from typing import Type

from racket import setup_logging, RacketBot

import discord
import discord.ext.commands


__all__ = ('run_cog',)


def run_cog(cog_class: Type[discord.ext.commands.Cog],
            *,
            token: str,
            guilds: Sequence[int] | None = None) -> None:
    """Runner function for your cog.

    Most bots implement a single Cog. This utility abstracts away all the logging,
    data, and bot construction, just running your cog for you.

    Your cog should inherit from discord.ext.commands.Cog, and it should take a
    single argument `racket.RacketBot`. racket.run_cog(...) will do the instatiation
    for you. This is to ensure that all logging is setup before the cog is
    initialized.

    ```
    import racket

    class MyCog(discord.ext.commands.Cog):
        def __init__(self, bot: racket.RacketBot):
            ...

    racket.run_cog(MyCog)
    ```
    """
    # Most importantly, do this as early as possible.
    setup_logging()
    log = logging.getLogger(__name__)

    intents = discord.Intents.default()
    intents.typing = False  # pylint: disable=assigning-non-slot
    intents.presences = False  # pylint: disable=assigning-non-slot
    intents.message_content = False  # pylint: disable=assigning-non-slot

    log.info('Creating bot object.')
    bot = RacketBot(intents=intents, guild_ids=guilds)

    log.info('Adding custom commands.')
    bot.add_cog(cog_class(bot))

    log.info('Starting the bot.')
    # Set the log_handler to avoid double logging settup.
    bot.run(token, log_handler=None)
