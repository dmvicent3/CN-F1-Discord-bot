import asyncio
import os
import pytest
import discord
from app import MyClient

from dotenv import load_dotenv
load_dotenv()


#SETUP THE CLIENT AND THE EVENT LOOP
async def client():
    
    client = MyClient(os.environ.get("DISCORD_TOKEN_TESTS"))
   
    loop = asyncio.get_event_loop()
    task = loop.create_task(client.run_bot_test())
    
    await asyncio.sleep(1) # Wait for the bot to become ready
    return client


#TEST IF THE BOT LOGGED IN SUCCESSFULLY
@pytest.mark.asyncio
async def test_start_bot():
    clt = await client()
    assert(clt.status == discord.Status.online)
    await clt.close()
 
#TEST COMMANDS
@pytest.mark.asyncio
async def test_drivers_command():   
    clt = await client()
    
    #SETUP THE CHAT TEST CHANNEL
    test_channel_id = os.environ.get("TEST_CHANNEL")
    test_channel = await clt.fetch_channel(test_channel_id)
    
    #SEND !drivers TO TEST CHANNEL
    message = "!drivers"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Points" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !constructors TO TEST CHANNEL
    message = "!constructors 2010"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Points" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !help TO TEST CHANNEL
    message = "!help"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("drivers" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !driver TO TEST CHANNEL
    message = "!driver Fernando Alonso"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Wiki" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !schedule TO TEST CHANNEL
    message = "!schedule"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Date" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !nextgp TO TEST CHANNEL
    message = "!nextgp"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("grandprix" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !circuits TO TEST CHANNEL
    message = "!circuits"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Country" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !circuit TO TEST CHANNEL
    message = "!circuit Hungaroring"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Wiki" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !last TO TEST CHANNEL
    message = "!last"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Driver" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !race TO TEST CHANNEL
    message = "!race 2003 5"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Driver" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !lastqual TO TEST CHANNEL
    message = "!lastqual"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Q1" in last_message)
    
    
    await asyncio.sleep(2) #WAIT FOR API COOLDOWN
    #SEND !qual TO TEST CHANNEL
    message = "!qual 2020 7"
    await test_channel.send(message)
    await asyncio.sleep(2) #WAIT FOR THE API TO RESPOND
    
    #CHECK THE LAST MESSAGE SENT IN THE CHANNEL
    response = [message async for message in test_channel.history(limit=1)]
    last_message = response[0].content
    assert("Q1" in last_message)
    await clt.close()


