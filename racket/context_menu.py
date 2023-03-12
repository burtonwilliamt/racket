"""Discord.py decide that context menus shouldn't be in a class.

I disagree. This is a helper method to do just that.
"""
import functools

import discord
import discord.app_commands

__all__ = ('context_menu',)

@functools.wraps(discord.app_commands.context_menu)
def context_menu(*args, **kwargs):
    """Sidestep discord.py\'s concern with context_menus being in classes.
    
    Uses the same arguments as discord.app_commands.context_menu(...).
    
    See this github issue with the reasoning for why discord.py doesnt support
    decorators.
    https://github.com/Rapptz/discord.py/issues/7823#issuecomment-1086830458
    """
    def decorator(func) -> discord.app_commands.ContextMenu:
        func.__cog_context_menu_args__ = (args, kwargs)
        return func

    return decorator