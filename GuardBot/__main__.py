# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger, INFO
from os import environ as env

from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from dotenv import load_dotenv
from rich.logging import RichHandler

if __name__ == '__main__':
    # Enables logging for Discord bot events
    basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]  # Pretty logger
    )

    getLogger('sqlachemy.engine').setLevel(INFO)

    # Create logging objects
    log = getLogger('rich')

    # Create bot object
    bot = Bot(
        command_prefix='g!',
        description='Prywatny bot Gwardii Gamerów.',
        owner_ids=[309270832683679745, 305025759356125184],
        # Q: What are intents?
        # A: https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents
        intents=Intents(
            guilds=True,
            guild_messages=True,
            guild_reactions=True,
            members=True,
            reactions=True
        )
    )

    # Create slash commands object
    slash = SlashCommand(bot)

    # Load environment variables from ".env" file
    load_dotenv()


    @bot.event
    async def on_ready():
        # Log bot's name
        log.info(f'Logged in as {bot.user}')

        # Load cogs
        for cog in [f'GuardBot.cogs.{cog}' for cog in [
            'basic', 'birthday'
        ]]:
            bot.load_extension(cog)

        # Sync slash commands
        await slash.sync_all_commands()


    # Start the bot
    bot.run(env.get('BOT_TOKEN'))
