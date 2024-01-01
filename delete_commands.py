import discord
from discord import app_commands
from login import discord_token

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1189134965766631476))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)
tree.clear_commands(guild=discord.Object(id = 1189134965766631476))

client.run(discord_token)