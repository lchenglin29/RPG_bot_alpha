import discord
import random
from discord.ext import commands
from core.core import Cog_Extension

class event(Cog_Extension):
  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author == self.bot.user:
      return
    if "Oksana" in message.content:
      msgs = ['去找她不要找我>:(','你的局;)','幫你@了不用客氣w','找你的:D']
      msg = random.choice(msgs)
      await message.channel.send(f'<@1232701498018762783> {msg}')
    if self.bot.user.mention in message.content:
      await message.channel.send('哈囉哈囉:D')
    
    
async def setup(bot):
    await bot.add_cog(event(bot))