import discord
from discord.ext import commands
from core.core import Cog_Extension

class cmd(Cog_Extension):
  @commands.command()
  async def Hello(self, ctx,co):
      await ctx.send(f'Hello, world!{co}')
    
async def setup(bot):
    await bot.add_cog(cmd(bot))