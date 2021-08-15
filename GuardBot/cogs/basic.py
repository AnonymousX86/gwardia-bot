# -*- coding: utf-8 -*-
from discord import Embed, Color
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash

from . import GUILD_IDS, PRIMARY_COLOR


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(
        name='test',
        description='Komenda testowa.',
        guild_ids=GUILD_IDS
    )
    async def test(self, ctx: SlashContext):
        await ctx.send('To jest komenda testowa.', embed=Embed(
            title='Gratulacje!',
            description='Jeżeli widzisz ten komunikat to znaczy, że bot działa poprawnie.',
            color=Color(PRIMARY_COLOR)
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ))


def setup(bot):
    bot.add_cog(Basic(bot))
