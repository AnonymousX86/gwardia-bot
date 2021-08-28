# -*- coding: utf-8 -*-
from asyncio import TimeoutError
from typing import Optional

from discord import Embed, Color, Message, Member
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option
from sqlalchemy.exc import OperationalError

from . import GUILD_IDS, PRIMARY_COLOR
from ..utils.database import get_birthday, del_birthday, set_birthday


class Birthday(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(
        name='urodziny',
        description='Zaktualizuj swoją datę urodzin.',
        guild_ids=GUILD_IDS,
        options=[create_option(
            name='osoba',
            description='Wybierz kogoś z serwera.',
            option_type=6,
            required=False
        )]
    )
    async def urodziny(self, ctx: SlashContext, osoba: Member = None):
        target_member = osoba or ctx.author

        def check(message: Message):
            return message.channel.id == ctx.channel.id and message.author.id == ctx.author_id

        async def timeout_message():
            await ctx.channel.send(embed=Embed(
                title=':x: Niepowodzenie',
                description='Następnym razem pisz trochę szybciej.',
                color=Color.red()
            ))

        await ctx.send('Uruchamiam menu...', hidden=True)
        msg = await ctx.channel.send(embed=Embed(
            title='Zarządzanie urodzinami',
            description='Co chcesz zrobić?',
            color=Color(PRIMARY_COLOR)
        ).add_field(
            name='Dostępne akcje',
            value='` 1 ` Dodaj/zmień\n` 2 ` Sprawdź\n` 3 ` Usuń'
        ).add_field(
            name='Wybrano',
            value=target_member.mention
        ).set_thumbnail(
            url=target_member.avatar_url
        ))
        try:
            response: Optional[Message] = await self.bot.wait_for('message', check=check, timeout=30)
        except TimeoutError:
            await timeout_message()
        else:
            choice = response.content
            await response.delete()

            # Dodawanie
            if choice == '1':
                em = Embed(
                    title=':inbox_tray: Dodawanie',
                    color=Color.green()
                )
                if target_member.id != ctx.author_id:
                    manager = ctx.author.guild_permissions.kick_members
                else:
                    # Ustawienie własnej daty urodzin
                    manager = True
                if not manager:
                    em.add_field(
                        name='Niepowodzenie',
                        value='Nie masz odpoiwednich uprawnień.'
                    )
                else:
                    selected = []
                    for x in ['miesiąca', 'dnia']:
                        if x.startswith('m'):
                            range_ = [1, 12]
                        elif (s := selected[0]) == 2:
                            range_ = [1, 29]
                        elif s in [1, 3, 5, 7, 8, 10, 12]:
                            range_ = [1, 31]
                        else:
                            range_ = [1, 30]
                        ask_msg = await ctx.channel.send('Podaj numer **{0}** (`{1[0]}`-`{1[1]}`)'.format(x, range_))
                        try:
                            response: Message = await self.bot.wait_for('message', check=check, timeout=30)
                        except TimeoutError:
                            await timeout_message()
                        else:
                            try:
                                select = int(response.content)
                                if select < range_[0] or select > range_[1]:
                                    raise ValueError
                            except ValueError:
                                em.add_field(
                                    name='Niepowodzenie',
                                    value='Podano nieprawidłowy numer **{0}**: `{1}`.'
                                          ' Spoza zakresu 1{2[0]}`-1{2[1]}1.'.format(x, response.content, range_)
                                )
                                break
                            else:
                                selected.append(select)
                            finally:
                                await ask_msg.delete()
                    if len(selected) == 2:
                        set_birthday(user_id=target_member.id, day=selected[1], month=selected[0])
                        em.add_field(
                            name='Sukces',
                            value='{0} ma urodziny w dniu `{1[1]}.{1[0]}`.'.format(target_member.mention, selected)
                        )
                await ctx.channel.send(embed=em)

            # Sprawdzanie
            elif choice == '2':
                try:
                    bday = get_birthday(user_id=target_member.id)
                except OperationalError:
                    await ctx.channel.send(embed=Embed(
                        title=':warning: Błąd',
                        description='Wystąpił błąd związany z bazą danych urodzin. ANON RATUJ.',
                        color=Color.gold()
                    ))
                else:
                    text = f'<@{bday.user_id}> ma urodziny: `{bday.date_day}.{bday.date_month}`' if bday \
                        else f'{target_member.mention} nie ma zapisanych urodzin'
                    await ctx.channel.send(embed=Embed(
                        title=':information_source: Sprawdzanie',
                        description=f'{text}.',
                        color=Color.blue()
                    ))

            # Usuwanie
            elif choice == '3':
                em = Embed(
                    title=':outbox_tray: Usuwanie',
                    color=Color.orange()
                )
                if target_member.id != ctx.author_id:
                    manager = ctx.author.guild_permissions.kick_members
                else:
                    manager = True
                if not manager:
                    em.add_field(
                        name='Niepowodzenie',
                        value='Nie masz odpoiwednich uprawnień.'
                    )
                elif bday := get_birthday(target_member.id):
                    del_birthday(target_member.id)
                    em.add_field(
                        name='Sukces',
                        value=f'Usunięto urodziny <@{bday.user_id}>.',
                        inline=False
                    )
                else:
                    em.add_field(
                        name='Niepowodzenie',
                        value=f'{target_member.mention} nie ma zapisanych urodzin.',
                        inline=False
                    )
                await ctx.channel.send(embed=em)

            # Błędna opcja
            else:
                await ctx.send(embed=Embed(
                    title=':no_entry_sign: Błąd',
                    description=f'Nieznana opcja: `{choice}`.',
                    color=Color.red()
                ))
        finally:
            await msg.delete()


def setup(bot):
    bot.add_cog(Birthday(bot))
