# -*- coding: utf-8 -*-
from discord import Embed, Color
from discord.ext.commands import Cog
from discord_slash import SlashContext, ComponentContext
from discord_slash.cog_ext import cog_slash
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component

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
            action_row = create_actionrow(
                create_button(
                    style=ButtonStyle.green,
                    label='Dodaj/zmień',
                    custom_id='change_bday'
                ),
                create_button(
                    style=ButtonStyle.red,
                    label='Usuń',
                    custom_id='delete_bday'
                )
            )
            await ctx.send(embed=Embed(
                title='Zarządzanie urodzinami'
            ), components=[action_row])
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            await button_ctx.edit_origin(embed=Embed(title=f'Kliknąłeś: `{button_ctx.custom_id}`'))


def setup(bot):
    bot.add_cog(Birthday(bot))
