# -*- coding: utf-8 -*-
from asyncio import TimeoutError
from typing import Optional

from discord import Embed, Color, Message
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash

from . import GUILD_IDS, PRIMARY_COLOR


class Birthday(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(
        name='urodziny',
        description='Zaktualizuj swoją datę urodzin.',
        guild_ids=GUILD_IDS
    )
    async def urodziny(self, ctx: SlashContext):
        if ctx.guild_id != 670766319372599297:
            await ctx.send(embed=Embed(
                title='Niedostępne',
                description='Ta komenda jest w fazie tworzenia.',
                color=Color(PRIMARY_COLOR)
            ))
        else:
            def check(message: Message):
                return message.channel.id == ctx.channel.id and message.author.id == ctx.author_id

            await ctx.send('Uruchamiam menu...', hidden=True)
            msg = await ctx.channel.send(embed=Embed(
                title='Zarządzanie urodzinami',
                description='Co chcesz zrobić?',
                color=Color(PRIMARY_COLOR)
            ).add_field(
                name='Dostępne akcje',
                value='` 1 ` Dodaj/zmień\n` 2 ` Usuń'
            ))
            try:
                response: Optional[Message] = await self.bot.wait_for('message', check=check, timeout=30)
            except TimeoutError:
                await ctx.channel.send(embed=Embed(
                    title=':x: Następnym razem pisz trochę szybciej',
                    color=Color.red()
                ))
            else:
                choice = response.content
                await response.delete()
                if choice == '1':
                    await ctx.channel.send(embed=Embed(
                        title=':green_circle: Dodawanie',
                        description='Funkcja w trakcie tworzenia.',
                        color=Color.green()
                    ))
                elif choice == '2':
                    await ctx.channel.send(embed=Embed(
                        title=':orange_circle: Usuwanie',
                        description='Funkcja w trakcie tworzenia.',
                        color=Color.orange()
                    ))
                else:
                    await ctx.send(embed=Embed(
                        title=':red_circle: Błąd',
                        description=f'Nieznana opcja: `{choice}`.',
                        color=Color.red()
                    ))
            finally:
                await msg.delete()


def setup(bot):
    bot.add_cog(Birthday(bot))
