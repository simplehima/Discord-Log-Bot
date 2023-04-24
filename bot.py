import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime



load_dotenv()

LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(LOG_CHANNEL_ID))
    embed = discord.Embed(title="Member Joined", description=f"{member.mention} joined the server.", color=discord.Color.green())
    embed.set_footer(text=f"User ID: {member.id} | Joined at {member.joined_at}")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(LOG_CHANNEL_ID))
    embed = discord.Embed(title="Member Left", description=f"{member.mention} left the server.", color=discord.Color.red())
    embed.set_footer(text=f"User ID: {member.id} | Left at {discord.utils.utcnow()}")
    await channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    admin_roles = ['Administrators', 'Administrators', 'Developers', 'move role'] # List of admin role names
    
    if before.channel != after.channel:
        if before.channel:
            # User left the channel
            message = f"{member.mention} left voice channel {before.channel.name}."
        if after.channel:
            # User joined the channel
            message = f"{member.mention} joined voice channel {after.channel.name}."
    else:
        # User moved to a different voice channel
        message = f"{member.mention} moved from {before.channel.name} to {after.channel.name}."
        
    # Check if admin moved or disconnected someone
    if any(role.name in admin_roles for role in member.roles):
        embed = discord.Embed(title="Admin Action", description=message, color=discord.Color.blue())
    else:
        embed = discord.Embed(title="User Action", description=message, color=discord.Color.green())

    # Add timestamp
    embed.timestamp = datetime.utcnow()

    # Send message to log channel
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if not after.author.bot:
        channel = bot.get_channel(int(LOG_CHANNEL_ID))
        embed = discord.Embed(title="Message Edited", description=f"{after.author.mention} edited a message in {after.channel.mention}", color=discord.Color.blue())
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"User ID: {after.author.id} | Edited at {discord.utils.utcnow()}")
        await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        channel = bot.get_channel(int(LOG_CHANNEL_ID))
        embed = discord.Embed(title="Message Deleted", description=f"{message.author.mention} deleted a message in {message.channel.mention}", color=discord.Color.red())
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"User ID: {message.author.id} | Deleted at {discord.utils.utcnow()}")
        await channel.send(embed=embed)

@bot.event
async def on_raw_message_edit(payload):
    # Check if the message was edited by the bot or if the message is from a DM
    if payload.author.bot or not payload.guild_id:
        return

    # Get the message's guild and log channel
    guild = bot.get_guild(payload.guild_id)
    log_channel = guild.get_channel(int(LOG_CHANNEL_ID))

    # Get the original message and the new message
    original_message = await log_channel.fetch_message(payload.message_id)
    new_message = await payload.channel.fetch_message(payload.message_id)

    # Create an embed to log the edited message
    embed = discord.Embed(title="Message Edited", description=f"Message edited in {payload.channel.mention}", color=0xFFA500)
    embed.add_field(name="Author", value=f"{new_message.author.mention} ({new_message.author})", inline=False)
    embed.add_field(name="Original Message", value=original_message.content, inline=False)
    embed.add_field(name="Edited Message", value=new_message.content, inline=False)
    embed.set_footer(text=f"Edited at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

    # Send the embed to the log channel
    await log_channel.send(embed=embed)

bot.run(TOKEN)
