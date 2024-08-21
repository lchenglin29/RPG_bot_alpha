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

async def start_g(interaction:discord.Interaction):
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
          description='很久很久以前，有這麼一座叫做Oltas的山\n\n因為其偏遠的地理位置，文明世界中幾乎沒有任何完整的記載\n只那麼幾篇冷門的史冊或地理書，會稍微提到他的存在\n\n不過，正是這樣，許多的傳說也因應而現',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='有人說，那座山中存放著遠古人類失傳的魔法杖，得到他便能使魔法重現於世\n\n有人說，那上面藏著歷代最偉大的探險家——Dotter Laice找到的所有寶藏。\n\n儘管不知道傳說的真實性，世界各地的冒險家們仍前仆後繼的試著找到這座山，和那所謂的魔杖與寶藏',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='然而，經歷數次的探索，冒險家們連這座山的確切地圖都畫不出來，更別提去找什麼寶藏了。\n\n喪氣的冒險家們放棄了這個虛無飄渺的傳說',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='不過，這群冒險家們並不知道，一個小村莊早已悄悄落在了這座山的其中一個山谷裡，過著寧靜、與世無爭的日子\n山谷中環境清幽、靜謐，且四季如春、長年溫煦\n村裡的居民於是幫這片世外桃源取了一個名字——「和風谷」',
          color=discord.Color.random()
        ),
        discord.Embed(
          description='少去那些文明帶來的喧囂與煩惱，村莊裡的每個人都親如一家，大家不分你我，一起分享這桃花源中的一切',
          color=discord.Color.random()
        )
      ]
      loading_emoji = load_json('emojis')["loading"]
      embed = discord.Embed(title=f'{loading_emoji} | 載入劇情中',color=discord.Color.gold())
      try:
        await interaction.response.send_message(embed=embed)
      except:
        pass
      await interaction.edit_original_response(embed=embed)
      for i in range(0,4):
        msg = f'即將開始播放初始劇情，倒數**{3-i}**秒'if i != 3 else '開始播放！'
        embed = discord.Embed(title='劇情載入完成！',description=msg,color=discord.Color.green())
        await interaction.edit_original_response(embed=embed)
        await asyncio.sleep(1)
      await interaction.edit_original_response(embed=pages[0])
      await asyncio.sleep(2)
      for i in pages[1:]:
        for j in range(1,8):
          i.set_footer(text=f'({j}/7)')
          await interaction.edit_original_response(embed=i)
          await asyncio.sleep(1)
      msg = "直到某天"
      embed = discord.Embed(
        description=msg,
        color=000000
      )
      await interaction.edit_original_response(embed=embed)
      for i in range(1,4):
        embed = discord.Embed(
        description=msg,
        color=000000
        )
        msg += "."
        await interaction.edit_original_response(embed=embed)
        
        await asyncio.sleep(0.5)
      await asyncio.sleep(0.5)
      embed = discord.Embed(
        description=msg+'\n一場暴雨過後\n你被劇烈的頭痛喚醒，發現自己位在一個完全陌生的地方',
        color=000000
      )
      await interaction.edit_original_response(embed=embed)
      await asyncio.sleep(5)
      await start_game_plot(interaction)
    except Exception as e:
      print(e)

async def start_game_plot(interaction:discord.Interaction):
  webhook_url = await check_wh(interaction.channel)
  async with aiohttp.ClientSession() as session:
    webhook = discord.Webhook.from_url(url=str(webhook_url),session=session)
    npc_info = load_json('npc_info')
#    [!] 記得完成新手劇情才能給劇情點免得出Bug
#    player = players(str(interaction.user.id))
#    player.plot_point.append('新手教學')
#    player.save_file()
#    原本是想再次挑戰翻頁的
    user_name = interaction.user.display_name
    avatar_url = interaction.user.avatar
    lines = [
      {
        'by':'w',
        'name': user_name,
        'avatar': avatar_url,
        'content':'...',
        'cooldown':2,
        'embed':None
      },
      {
        'by':'w',
        'name': user_name,
        'avatar': avatar_url,
        'content':'頭好痛...',
        'cooldown':1,
        'embed':None
      },
      {
        'by':'b',
        'content':None,
        'embed':discord.Embed(
          description='你扶著牆，掙扎著站起身',
          color=discord.Color.red()
        ),
        'cooldown':0.5
      },
      {
        'by':'w',
        'name': user_name,
        'avatar': avatar_url,
        'content':'這裡是...哪裡？',
        'cooldown':1,
        'embed':None
      },
      {
        'by':'w',
        'name': user_name,
        'avatar': avatar_url,
        'content':'\*自言自語\*：也許可以先看看周圍？',
        'embed':None,
        'cooldown':1
      },
      {
        'by':'b',
        'content':None,
        'embed':discord.Embed(
          title='[!提示!]',
          description='使用 /地圖 以查看所處地圖周圍',
          color=discord.Color.gold()
        ),
        'cooldown':0.5
      }
    ]
    for line in lines:
      if line['by'] == 'w':
        await webhook.send(
          username=line['name'],
        avatar_url=line['avatar'],
          content=line['content'],
          embed=line['embed']
      )
      elif line['by'] == 'b':
        await interaction.channel.send(
          line['content'],
          embed=line['embed']
        )
      await asyncio.sleep(line['cooldown'])

async def start_game_after_map(interaction:discord.Interaction):
  webhook_url = await check_wh(interaction.channel)
  async with aiohttp.ClientSession() as session:
    webhook = discord.Webhook.from_url(url=str(webhook_url),session=session)
    npc_info = load_json('npc_info')
    user_name = interaction.user.display_name
    avatar_url = interaction.user.avatar
    lines = [
      {
        'by':'b',
        'content':None,
        'embed':discord.Embed(
          description='你環顧四週，遠方似乎有個出口',
          color=discord.Color.green()
        ),
        'cooldown':1
      },
      {
        'by':'w',
        'name': user_name,
        'avatar': avatar_url,
        'content':'\*自言自語：\*那是什麼？我想過去看看',
        'embed':None,
        'cooldown':1        
      },
      {
        'by': 'b',
        'content':None,
        'embed':discord.Embed(
          title='[!提示!]',
          description='使用 /地圖 時，若出現按鈕，即為可互動之設施！\n請再次使用地圖！',
          color=discord.Color.gold()
        ),
        'cooldown':1
      }
    ]
    for line in lines:
      if line['by'] == 'w':
        await webhook.send(
          username=line['name'],
        avatar_url=line['avatar'],
          content=line['content'],
          embed=line['embed']
      )
      elif line['by'] == 'b':
        await interaction.channel.send(
          line['content'],
          embed=line['embed']
        )
      await asyncio.sleep(line['cooldown'])
    player = players(str(interaction.user.id))
    player.plot_point.append('新手教學')
    player.plot_point.append('地圖教學')
    player.save_file()

class app_cmd(Cog_Extension):
  @app_commands.command(name="開始遊戲",description='若創建存檔後未自動播放初始劇情，請使用此指令')
  async def start_game(self,interaction:discord.Interaction):
    await start_g(interaction)

  @app_commands.command(name="地圖",description='查看地圖')
  async def map(self,interaction:discord.Interaction):
    try:
      player = players(str(interaction.user.id))
      avatar = player.avatar
      map = load_json("maps")[player.location]["map"]
      msg = ''
      for i in map:
        for j in i:
          if j == '{avatar}':
            msg += f'{avatar}'
            continue
          msg += j
      embed = discord.Embed(
        title=f'{avatar} | {player.location}',
        description=msg,
        color=discord.Color.gold()
      )
      if '地圖教學' not in player.plot_point:
        await interaction.response.send_message(embed=embed)
        await start_game_after_map(interaction)
        return
      else:
        view = discord.ui.View()
        await interaction.response.send_message(embed=embed)
    except Exception as e:
      embed = discord.Embed(
        title='蛤',
        description='你目前沒有遊玩任何存檔',
        color=discord.Color.red()
      )
      print(e)
      await interaction.response.send_message(embed=embed)
    return
async def setup(bot):
    await bot.add_cog(app_cmd(bot))