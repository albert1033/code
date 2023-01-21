import discord
from discord.ext import commands
from discord.ext.commands import slash_command
import json
import datetime, time
from config import *
from discord.ui import Button, View
import time
from datetime import date
class user(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @slash_command(description = "Link Start!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def start(self, ctx):
        await ctx.defer()
        with open('users.json', 'r') as f:
            user = json.load(f)
        
        if str(ctx.author.id) in user:
            embed = discord.Embed(title = "Error!", description="You already created an account!", color = discord.Color.red())
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            await ctx.respond(embed = embed)

        else:
            yes_btn = Button(label="Yes", style = discord.ButtonStyle.green)
            no_btn = Button(label="No", style = discord.ButtonStyle.red)
            view = View()
            view.add_item(yes_btn)
            view.add_item(no_btn)
            async def yes_callback(interaction):
                #await interaction.response.defer()
                if interaction.user != ctx.author:
                    await interaction.response.send_message("You can't do that!", ephemeral = True)
                else:
                    user[str(ctx.author.id)] = {"date": str(date.today().strftime("%B %d, %Y")), "time": time.time()}
                    with open('users.json', 'w') as f:
                        json.dump(user, f, indent = 4)

                    success_embed = discord.Embed(title = "Success!", description=f"You have created an account !", color = discord.Color.green())
                    success_embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    await interaction.response.edit_message(embed = success_embed, view = None)

            async def no_callback(interaction):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("You can't do that!", ephemeral = True)

                else:
                    fail_embed = discord.Embed(title = "Fail!", description = "You have declined creating a new account!", color = discord.Color.red())
                    fail_embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    await interaction.response.edit_message(embed = fail_embed, view = None)
            
            yes_btn.callback = yes_callback
            no_btn.callback = no_callback
                
            ask_embed = discord.Embed(title = "Create account!", description = "Do you agree to create an account? If yes, you agreed to allow us to store your Discord User ID", color = discord.Color.blurple())
            ask_embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            ask_embed.set_image(url = "https://media3.giphy.com/media/Kr2m7wuAZDNISVTLyt/giphy.gif?cid=ecf05e47mnnah8dgprivna47qr7k7f68yf2kulecq8mbx8ns&rid=giphy.gif&ct=g")
            await ctx.respond(embed = ask_embed, view = view)

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()
    
    @slash_command(description = "Check your profile!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member):
        await ctx.defer()
        with open("users.json", 'r') as f:
            user = json.load(f)
        if str(member.id) in user:
            embed = discord.Embed(title = f"{member.name}'s profile",
            description=f"""```yaml
Name: {member.name}#{member.discriminator}
ID: {member.id}
Started: {user[str(member.id)]["date"]} [{str(datetime.timedelta(seconds=int(round(time.time() - user[str(member.id)]["time"]))))} ago]
```""" ,color = discord.Color.green())
            embed.set_thumbnail(url = member.avatar.url)
            user = await self.client.fetch_user(member.id)
            embed.set_image(url = user.banner.url if user.banner is not None else "https://media1.giphy.com/media/kFgzrTt798d2w/giphy.gif?cid=ecf05e47demj4pecfuv41re0g1mbdu2vb8i6l28iw7n0292g&rid=giphy.gif&ct=g")
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            await ctx.respond(embed = embed)
        else:
            if member.id == ctx.author.id:
                embed = discord.Embed(title = "Error!", description = "You haven't created an account! use `/start` to create one!", color = discord.Color.red())
                embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.respond(embed = embed)
            else:
                embed = discord.Embed(title = "Error!", description="This user hasn't created an account!", color = discord.Color.red())
                embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(user(bot))