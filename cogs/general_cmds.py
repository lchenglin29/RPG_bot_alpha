import discord
from discord.ext import commands
from core.core import Cog_Extension

class cmd(Cog_Extension):
  @commands.command()
  async def hello(self, ctx,co):
      await ctx.send(f'Hello, world! {co}')

  @commands.command()
  async def ping(self, ctx):
      await ctx.send(f'當前延遲：{round(self.bot.latency*1000)} (ms)')

  @commands.command()
  async def say(self, ctx, *, msg):
      await ctx.message.delete()
      await ctx.send(msg)
async def setup(bot):
    await bot.add_cog(cmd(bot))