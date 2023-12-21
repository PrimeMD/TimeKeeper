import discord
from discord import app_commands
from config import config
import logging


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild_id in config["bot"]["preferred_guilds"]:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)


client = MyClient()
logging.debug("inizialized Discord Client")
