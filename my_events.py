import discord
from discord.ext import commands
from discord.message import Message
from leveling_system import LevelingSystem

class DiscordEvents(commands.Cog):

    def __init__(self, bot: commands.Bot, ls: LevelingSystem) -> None:
        self.bot = bot
        self.ls = ls

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Alive! {self.bot.user}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel != after.channel and before.channel != None and after.channel != None:
            print(f"Member {member.display_name} has joined from channel \"{before.channel}\" to channel \"{after.channel}\"")
        elif before.channel != after.channel:
            if after.channel == None:
                print(f"{member.display_name} left the channel {before.channel}")
            else:
                print(f"{member.display_name} joined the channel {after.channel}")
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author != self.bot.user:
            lvlup = await self.ls.update_level(message.author)
            await self.ls.add_xp(user = message.author)
            if lvlup:
                await message.reply(f"Congrats! You leveled up to level {self.ls._get_level(message.author)[0][2]}")