from dotenv import load_dotenv
load_dotenv()
import os
import discord
from commands import commands

class MyClient(discord.Client):
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.token = token

    async def on_ready(self):
        print('Logged in as', self.user)
        

    async def on_message(self, message):
        if message.content.startswith('!'):
            command = message.content[1:] # Remove the "!" from the message content
            if command in commands:
                await commands[command](message)

    def run_bot(self):
        self.run(self.token)
        
    def run_bot_test(self):
        return self.start(self.token)


if __name__ == '__main__':
    bot = MyClient(os.environ.get("DISCORD_TOKEN"))
    bot.run_bot()
