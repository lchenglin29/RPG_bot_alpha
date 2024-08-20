import discord,asyncio,aiohttp
from discord import app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js
from objects.player_object import players,users


async def check_wh(channel):
  data = load_json('channels')
  channel_id = str(channel.id)
  if channel_id in data["channel_url"]:
    return str(data["channel_url"][channel_id])
  elif channel_id not in data["channel_url"]:
    webhook = await channel.create_webhook(name='rpg_bot')
    await webhook.send(content='Webhook初始化中！\n（可以忽略我沒關係:D',username='Koala',avatar_url=load_json('npc_info')['Koala']['avatar'])
    data["channel_url"].setdefault(channel_id,str(webhook.url))
    write_js('channels',data)
    return str(webhook.url)

async def start_game_plot(interaction:discord.Interaction):
  loading_emoji = load_json('emojis')["loading"]
  embed = discord.Embed(title=f'{loading_emoji} | 載入劇情中',color=discord.Color.gold())
  await interaction.edit_original_response(embed=embed)
  webhook_url = await check_wh(interaction.channel)
  async with aiohttp.ClientSession() as session:
    webhook = discord.Webhook.from_url(url=str(webhook_url),session=session)
    npc_info = load_json('npc_info')
    for i in range(0,4):
      msg = f'即將開始播放初始劇情，倒數**{3-i}**秒'if i != 3 else '即將開始播放初始劇情'
      embed = discord.Embed(title='劇情載入完成！',description=msg,color=discord.Color.green())
      await interaction.edit_original_response(embed=embed)
      await asyncio.sleep(1)
#    [!] 記得完成新手劇情才能給劇情點免得出Bug
#    player = players(str(interaction.user.id))
#    player.plot_point.append('新手教學')
#    player.save_file()
#    原本是想再次挑戰翻頁的
    
    await interaction.channel.send("測試")
    await webhook.send(content='我才沒有喜歡你呢\n這在俄羅斯很正常',username='艾莉',avatar_url=npc_info['Alya']['avatar'])
    await webhook.send(content='<:alya_shy:1274956816744185927>',username='艾莉',avatar_url=npc_info['Alya']['avatar'])

class app_cmd(Cog_Extension):
  @app_commands.command(name="開始遊戲",description='若創建存檔後未自動播放初始劇情，請使用此指令')
  async def start_game(self,interaction:discord.Interaction):
    try:
      user = users(str(interaction.user.id))
      if not user.save:
        await interaction.response.send_message('你並未遊玩任何存檔')
        return
      elif '新手教學' in user.saves[user.save[0]]['plot_point']:
        await interaction.response.send_message('沒人在看兩次新手教學的吧老哥')
        return
      pages = [
        discord.Embed(
          title='【第一章 序曲】',
          description='即將開始播放！',
          color=discord.Color.gold(),
        ),
        discord.Embed(
          description='很久很久以前，在一座不知何處的偏遠深山裡',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='一個小村莊悄悄的落在了這座山的其中一個山谷裡，過著寧靜、與世無爭的日子\n山谷中環境清幽、靜謐，且四季如春、長年溫煦\n村裡的居民於是幫這片世外桃園取了一個名字——「和風谷」',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='因為沒有那些都市的喧囂與煩惱，村莊裡的每個人都親如一家，大家不分你我，一起分享這桃花源中的一切',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='直到有一天，「帝國」盯上了這一切\n\n於是，帝國的皇帝——厄瑞洛斯 Erilos派出了他的爪牙作為先鋒，準備將和風谷納入帝國的版圖'
          ,color=discord.Color.red()
        ),
        discord.Embed(
          description='這匹探路的先鋒隊，被稱為「夜行者 Nightstalkers」\n\n就這樣，一場風暴悄悄地靠近和風谷',
          color=000000
        ),
        discord.Embed(
          description='某天...'
        )
      ]
      await interaction.response.send_message(embed=pages[0])
      await asyncio.sleep(2)
      for i in pages[1:]:
        for j in range(1,6):
          i.set_footer(text=f'({j}/5)')
          await interaction.edit_original_response(embed=i)
          await asyncio.sleep(1)
      await start_game_plot(interaction)
    except Exception as e:
      print(e)

async def setup(bot):
    await bot.add_cog(app_cmd(bot))