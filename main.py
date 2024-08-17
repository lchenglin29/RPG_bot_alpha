import discord
from discord.ext import commands
import os,asyncio,datetime, pytz,aiohttp
bot_token = os.environ['bot_token']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='r!', intents= intents)

def now_time():
    current_time = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Taipei')
    localized_time = current_time.astimezone(timezone)
    return localized_time.strftime("%Y-%m-%d %H:%M")

def textmsg(user):
  return f'回覆:{user} | 時間:{now_time()}'

@bot.event
async def on_ready():
  await bot.tree.sync()
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="/開始遊戲", url="https://youtu.be/dQw4w9WgXcQ"))

  print(f'{bot.user}已上線。')

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"已載入{extension}")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"已卸載{extension}")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"已重新載入{extension}")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(title=':x:哎呀，有問題:(',description='必要參數缺失',color=0xff0000)
    embed.set_footer(text=textmsg(ctx.author.display_name))
    await ctx.reply(embed=embed)
  elif isinstance(error, commands.CommandNotFound):
    embed = discord.Embed(title=':x:哎呀，有問題:(',description='找不到這個指令',color=0xff0000)
    embed.set_footer(text=textmsg(ctx.author.display_name))
    await ctx.reply(embed=embed)
  elif isinstance(error, commands.CommandOnCooldown):
    message = f'再等 {error.retry_after:.0f} 秒啦'
    await ctx.reply(message)
  else: 
    await ctx.reply(f'我不知道你在供三小:({error}')

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())