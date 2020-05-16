import discord
from discord.ext import commands
import setup
from discord.utils import get
from discord import FFmpegPCMAudio
import os.path
import os


description = "Type !pokemon <pokemon> to play their cries."
TOKEN = setup.TOK
client = commands.Bot(command_prefix='!', description=description, help_command=None)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    initcount = 0
    for g in client.guilds:
        initcount = initcount + len(g.members)
    game = discord.Game("i play music now bitches")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_guild_join(guild):
    print("Joined New Server: " + guild.name + ". Members: " + str( len(guild.members) ) + ". Owner: " + guild.owner.display_name + ".")

@client.event
async def on_guild_remove(guild):
    print("Removed From Server: " + guild.name + ". Members: " + str( len(guild.members) ) + ". Owner: " + guild.owner.display_name + ".")

    
@client.event
async def on_message(message):
    if message.author == client.user:   
        return       
    await client.process_commands(message)

@client.command()
async def pokemon(ctx, pkmn):
    audio_path = "./audio_files/" + pkmn.lower() + ".mp3"
    if not os.path.exists(audio_path):
        await ctx.send("pokemon doesnt exist or is too new - this has everything on pkmnshowdown")
        return
    await ctx.send("Playing " + pkmn + "'s cry")
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio(audio_path)
    player = voice.play(source)
    

client.run(TOKEN)
            