import asyncio
import os
import pytest
import discord
from app import MyClient

from dotenv import load_dotenv
load_dotenv()


#SETUP THE CLIENT AND THE EVENT LOOP
async def client():
    
    client = MyClient(os.environ.get("DISCORD_TOKEN"))
   
    loop = asyncio.get_event_loop()
    task = loop.create_task(client.run_bot_test())
    
    await asyncio.sleep(1) # Wait for the bot to become ready
    return client


#TEST IF THE BOT LOGGED IN SUCCESSFULLY
@pytest.mark.asyncio
async def test_start_bot():
    clt = await client()
    assert(clt.status == discord.Status.online)
    
 
#TEST IF THE !drivers COMMAND WAS RESPONDED TO 
@pytest.mark.asyncio
async def test_drivers_command():   
    clt = await client()
    
    #SETUP THE CHAT TEST CHANNEL
    test_channel_id = os.environ.get("TEST_CHANNEL")
    test_channel = await clt.fetch_channel(test_channel_id)
    
    #SEND !drivers TO TEST CHANNEL
    message = "!drivers"
    await test_channel.send(message)
    await asyncio.sleep(1) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Points" in last_message)
