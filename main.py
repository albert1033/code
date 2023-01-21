import discord
from discord.ext import commands
import os

bot = discord.Bot(intents = discord.Intents.default())

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
  
bot.run("TOKEN")