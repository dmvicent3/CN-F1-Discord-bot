import os
from dotenv import load_dotenv
load_dotenv()

import discord
from commands import commands

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as', self.user)

    async def on_message(self, message):

        if message.content.startswith('!'):
            command = message.content[1:] # Remove the "!" from the message content
            if command in commands:
                await commands[command](message)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.environ.get("DISCORD_TOKEN"))