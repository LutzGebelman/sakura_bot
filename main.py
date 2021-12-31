from discord.ext import commands
from my_events import DiscordEvents
from my_commands import DiscordCommands
from leveling_system import LevelingSystem
import json
config = json.loads(open("config.json").read())
token = config['credentials']['ds_token']

bot = commands.Bot("s!", help_command=None)

ls = LevelingSystem()

bot.add_cog(DiscordCommands(bot, ls))
bot.add_cog(DiscordEvents(bot, ls))

commands_instance = bot.get_cog("DiscordCommands")
events_instance = bot.get_cog("DiscordEvents")

bot.run(token)