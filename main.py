import discord
import random
import aiohttp
import datetime
import platform
from discord.ext import commands
from Pickup_Lines import pickups
from Sensitive_Info import TOKEN

PREFIX = "&"
client = commands.Bot(description="Basic Bot by Joe", command_prefix=PREFIX, pm_help=False, case_insensitive = True)
session = aiohttp.ClientSession()# Do this once, at startup or right before the first command

@client.event
async def on_ready():
    print('Logged in as ' + str(client.user.name) + ' (ID:' + str(client.user.id) + ') | Connected to ' + str(len(client.guilds)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')

    await client.change_presence(game=discord.Game(name=PREFIX + " On " + str(len(client.guilds)) + " Servers"))


@client.command()
async def ping(ctx):
    """Ping the bot, showing its status and round-trip time."""
    msg = await ctx.send(":ping_pong: Pong!")
    delay = msg.created_at - ctx.message.created_at
    await msg.edit(content='{}\nRound-trip: {}ms'.format(msg.content, delay.seconds * 1000 + delay.microseconds / 1000))
    await ctx.send("API Latency is: " + str(round(client.latency, 4)*1000) + "ms")

@client.command()
async def pickUp(ctx):
    """Gives a random pickup line from a file"""
    await ctx.send(pickups[random.randint(0,pickups.__len__()-1)])

@client.command()
@commands.has_role("Moderator")
async def tell(ctx, user : discord.Member):
    """A fun gift to give to someone"""
    for x in range(15):
        await ctx.author.send("Hello")

@client.command()
async def req(ctx, teamNum : str):
    """Request the name of an FRC team by putting in a number"""
    url = 'https://www.thebluealliance.com/api/v3/team/frc' + teamNum + '/simple'
    headers = {'X-TBA-Auth-Key': 'ZND1hBIq0WU6su8VYVfsUrJ18evzHcqNi0eSqWbYepY798Oq7ZR6CVAsuZ1ZF6HH'}
    async with session.get(url, headers=headers) as resp:
        response = await resp.json()
        if(resp.status == 404):
            await ctx.send('This team does not exist')
        else:
            await ctx.send(response['nickname'])

@client.command()
async def dice(ctx, number_of_rolls : int, sides : int):
    """Roll x times of a y sided die"""
    results = []
    for x in range(number_of_rolls):
        num = random.randint(1, sides)
        results.append(num)
    await ctx.send(results)

@client.command()
async def hug(ctx, member : discord.Member):
    """Give someone a hug"""
    await ctx.send("https://media.giphy.com/media/XpgOZHuDfIkoM/giphy.gif")
    await ctx.send("Have a hug {0.name}".format(member))

@client.command()
@commands.has_role("Moderator")
async def changeStatus(ctx, status : str):
    """Change the status of the bot"""
    await client.change_presence(game=discord.Game(name=status))

@client.command()
async def timeCheck(ctx):
    """Give the time in four digits"""
    now = datetime.datetime.now()
    number = (now.hour*100)+now.minute
    await ctx.send(number)

@client.command()
async def shutdown(ctx):
    """Shut down the bot???"""
    await ctx.send("Shutting Down")
    await client.logout()

@client.command()
@commands.has_role("Moderator")
async def speak(ctx, input : str):
    """Use TTS to annoy everybody in said channel"""
    await ctx.send(input, tts=True)

@client.command()
async def hat(ctx):
    """Hat"""
    await ctx.send("https://www.youtube.com/watch?v=vyVkyakC6xk")


''''@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
'''
client.run(TOKEN)