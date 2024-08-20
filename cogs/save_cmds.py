from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from objects.player_object import users, players
from typing import Optional

class save_cmds(Cog_Extension):
  
  @app_commands.command(name = "創建存檔", description = "創建一個新存檔")
  async def create_save(self, interaction: discord.Interaction,avatar:str):
      user = users(str(interaction.user.id))
      class Modal(discord.ui.Modal, title="創建存檔"):
          save_name = discord.ui.TextInput(
              label = "輸入存檔名稱",
              style = discord.TextStyle.short,
              max_length = 5
          )
          player_name = discord.ui.TextInput(
              label = "輸入玩家名稱",
              style = discord.TextStyle.short
          )
          async def on_submit(self, interaction: discord.Interaction):
              if self.save_name.value in user.saves:
                  embed = discord.Embed(title=':x:哎呀，有問題:(',description='這個存檔名稱已經被使用過',color=discord.Color.red())
                  await interaction.response.send_message(embed=embed)
                  return
              user.create_save(self.save_name.value,self.player_name.value,avatar)
              if len(user.save) == 0:
                  user.save.append(self.save_name.value)
                  msg = "已將你自動切換至該存檔！"
                  user.save_file()
              else:
                  msg = "輸入指令來切換存檔！"
              embed = discord.Embed(
                  title="存檔創建成功！",
                  description=msg,
                  color=discord.Color.green()
              )
              print('?')
              await interaction.response.send_message(embed=embed)
      await interaction.response.send_modal(Modal())
  
  @app_commands.command(name="玩家資訊",description="查看玩家資訊")
  async def player_info(self,interaction:discord.Interaction,user:Optional[discord.Member]=None):
      if user == None:
          user = interaction.user
      user = users(str(user.id))
      embed = discord.Embed(
          title=f"{interaction.user.display_name}的遊戲檔案",
          description=f"存檔數量{len(user.saves)}",
          color=discord.Color.random()
      )
      embed.add_field(name='用戶ID',value=str(user.id))
      msg = user.save[0] if user.save else '無正在遊玩存檔'
      embed.add_field(name='當前遊玩存檔',value=msg)
      msg='空空如也'
      if len(user.badge) > 0:
        msg = '\n'.join(user.badge)
      embed.add_field(name='徽章',value=msg)
      msg = '\n'.join(f'{i+1}. {user.saves[key]["avatar"]}{key}' for i, key in enumerate(user.saves.keys())) if user.saves else '空空如也'
      embed.add_field(name='存檔列表：' ,value=msg)
      await interaction.response.send_message(embed=embed)

  @app_commands.command(name="切換存檔",description="切換存檔")
  async def switch_save(self,interaction:discord.Interaction,save_name:str):
      user = users(str(interaction.user.id))
      if save_name in user.saves:
        user.save[0] = save_name
        user.save_file()
        embed = discord.Embed(
            title="存檔切換成功！",
            description=f"已切換至{save_name}存檔",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
      else:
        embed = discord.Embed(
            title="無法切換存檔！",
            description=f"找不到{save_name}存檔",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
      
    
async def setup(bot):
    await bot.add_cog(save_cmds(bot))