import discord
from discord.colour import Color
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.member import User as MemberUser
from giphy_api import GiphyApi
from leveling_system import LevelingSystem

class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, ls: LevelingSystem) -> None:
        self.bot = bot
        self.ls = ls
        self.giphy_session = GiphyApi()

    # @commands.slash_command()
    # async def listgames(self, ctx: ApplicationContext):
    #     response = ctx.response
    #     await response.send_message("Fuck you")

    @commands.slash_command(description="Will return you random gif from the internet by query. Powered by giphy")
    async def giphy(self, ctx: ApplicationContext, query: str):
        response = ctx.response
        await response.send_message(self.giphy_session.search(query))

    @commands.slash_command(description="Ban the user from the guild")
    async def ban(self, ctx: ApplicationContext, user: MemberUser):
        response = ctx.response
        try:
            if discord.Permissions.ban_members not in ctx.user.guild_permissions:
                await ctx.response.send_message("You don't have permissions to do that!")
            else:
                await ctx.guild.ban(user, reason="Testing")
                await response.send_message(f"User {user} has been baned from the server")
        except discord.DiscordException as err:
            await response.send_message(f"Can't do that do to the following reson:\n{err}")

    @commands.slash_command(description="Unban the user from the guild")
    async def unban(self, ctx: ApplicationContext, user: MemberUser):
        response = ctx.response
        try:
            if discord.Permissions.ban_members not in ctx.user.guild_permissions:
                await ctx.response.send_message("You don't have permissions to do that!")
            else: 
                if type(user) == int:
                    user = await self.bot.fetch_user(user)
                await ctx.guild.unban(user)
                await response.send_message(f"User {user} has been unbaned")
        except discord.DiscordException as err:
            await response.send_message(f"Can't do that do to the following reson:\n{err}")
    
    @commands.slash_command(description="Kicks the member from the guild")
    async def kick(self, ctx: ApplicationContext, user: MemberUser):
        response = ctx.response
        try:
            if discord.Permissions.kick_members not in ctx.user.guild_permissions:
                await ctx.response.send_message("You don't have permissions to do that!")
            else:
                await ctx.guild.kick(user, reason="Testing")
                await response.send_message(f"User {user} has been kicked from the server")
        except discord.DiscordException as err:
            await response.send_message(f"Can't do that do to the following reson:\n{err}")

    @commands.slash_command(description="Just a command for testing different stuff")
    async def testing(self, ctx: ApplicationContext, user: MemberUser):
        if type(user) == int:
            user = await self.bot.fetch_user(user)
        print(user)
        await ctx.response.send_message(user)

    @commands.slash_command(description="Shows you the help message")
    async def help(self, ctx: ApplicationContext):
        text = f'''
        Hello there! My name is sakura. All my commands are slashable 
        I have these commands:
        /giphy -- fetches random gif of your choice from internet
        /ban -- ban member
        /unban -- unban member
        /kick -- kick member
        /my_level -- Will return your level
        /my_xp -- Will return your XP
        '''
        embed = discord.Embed(description = text, color = Color.purple())
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="Turns the bot off, only for bot owner")
    @commands.is_owner()
    async def _off_yourself(self, ctx :ApplicationContext):
        await self.bot.close() 

    @commands.slash_command(description="Returns the level you're curently on")
    async def my_level(self, ctx: ApplicationContext):
        await ctx.response.send_message(f"You are curenbly on the level {self.ls._get_level(ctx.author)[0][2]}")

    @commands.slash_command(description="Returns how much XP you have")
    async def my_xp(self, ctx: ApplicationContext):
        await ctx.response.send_message(f"You curently have {self.ls._get_level(ctx.author)[0][1]}xp")

    