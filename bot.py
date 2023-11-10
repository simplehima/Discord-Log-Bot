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
    admin_roles = ['Administrators', 'Developers', 'move role']  # List of admin role names

    # Check if the user was self-muted or self-deafened
    if before.self_mute != after.self_mute:
        if after.self_mute:
            message = f"{member.mention} self-muted."
        else:
            message = f"{member.mention} self-unmuted."

        embed = discord.Embed(title="User Action", description=message, color=discord.Color.green())
        embed.timestamp = datetime.utcnow()
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=embed)

    if before.self_deaf != after.self_deaf:
        if after.self_deaf:
            message = f"{member.mention} self-deafened."
        else:
            message = f"{member.mention} self-undeafened."

        embed = discord.Embed(title="User Action", description=message, color=discord.Color.green())
        embed.timestamp = datetime.utcnow()
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=embed)

    # Check if the user was moved to a different channel
    if before.channel != after.channel:
        if before.channel:
            # User left the channel
            message = f"{member.mention} left voice channel {before.channel.name}."
        if after.channel:
            # User joined the channel
            message = f"{member.mention} joined voice channel {after.channel.name}."

        embed = discord.Embed(title="User Action", description=message, color=discord.Color.green())
        embed.timestamp = datetime.utcnow()
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=embed)

    # Check if someone else (admin) muted or deafened the user
    if any(role.name in admin_roles for role in member.roles):
        if before.mute != after.mute:
            if after.mute:
                message = f"{member.mention} was server-muted by an admin."
            else:
                message = f"{member.mention} was server-unmuted by an admin."

            embed = discord.Embed(title="Admin Action", description=message, color=discord.Color.blue)
            embed.timestamp = datetime.utcnow()
            log_channel = bot.get_channel(log_channel_id)
            await log_channel.send(embed=embed)

        if before.deaf != after.deaf:
            if after.deaf:
                message = f"{member.mention} was server-deafened by an admin."
            else:
                message = f"{member.mention} was server-undeafened by an admin."

            embed = discord.Embed(title="Admin Action", description=message, color=discord.Color.blue)
            embed.timestamp = datetime.utcnow()
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
    if payload.data.get('author') and not payload.data['author']['bot']:
        # Get the message's guild and log channel
        guild = bot.get_guild(payload.data['guild_id'])
        log_channel = guild.get_channel(int(LOG_CHANNEL_ID))

        # Get the original message and the new message
        try:
            original_message = await log_channel.fetch_message(payload.message_id)
            new_message = await payload.channel.fetch_message(payload.message_id)

            # Create an embed to log the edited message
            embed = discord.Embed(title="Message Edited", description=f"Message edited in {payload.data['channel_id']}", color=0xFFA500)
            embed.add_field(name="Author", value=f"{new_message.author.mention} ({new_message.author})", inline=False)
            embed.add_field(name="Original Message", value=original_message.content, inline=False)
            embed.add_field(name="Edited Message", value=new_message.content, inline=False)
            embed.set_footer(text=f"Edited at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

            # Send the embed to the log channel
            await log_channel.send(embed=embed)
        except Exception as e:
            print(e)

@bot.event
async def on_guild_channel_delete(channel):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    channel_name = channel.name
    embed = discord.Embed(title="Channel Deleted", description=f"Channel '{channel_name}' was deleted.", color=discord.Color.red())
    embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    if before.name != after.name:
        embed = discord.Embed(title="Channel Renamed", description=f"Channel '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue())
    else:
        embed = discord.Embed(title="Channel Edited", description=f"Channel '{before.name}' was edited.", color=discord.Color.blue())
    embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_create(role):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    role_name = role.name
    embed = discord.Embed(title="Role Created", description=f"Role '{role_name}' was created.", color=discord.Color.green())
    embed.set_footer(text=f"Guild ID: {role.guild.id} | Created at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_delete(role):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    role_name = role.name
    embed = discord.Embed(title="Role Deleted", description=f"Role '{role_name}' was deleted.", color=discord.Color.red())
    embed.set_footer(text=f"Guild ID: {role.guild.id} | Deleted at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_update(before, after):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    if before.name != after.name:
        embed = discord.Embed(title="Role Renamed", description=f"Role '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue())
    else:
        embed = discord.Embed(title="Role Edited", description=f"Role '{before.name}' was edited.", color=discord.Color.blue())
    embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    channel_name = channel.name
    embed = discord.Embed(title="Channel Created", description=f"Channel '{channel_name}' was created.", color=discord.Color.green())
    embed.set_footer(text=f"Guild ID: {channel.guild.id} | Created at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    channel_name = channel.name
    embed = discord.Embed(title="Channel Deleted", description=f"Channel '{channel_name}' was deleted.", color=discord.Color.red())
    embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
    if before.name != after.name:
        embed = discord.Embed(title="Channel Renamed", description=f"Channel '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue())
    else:
        embed = discord.Embed(title="Channel Edited", description=f"Channel '{before.name}' was edited.", color=discord.Color.blue())
    embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.utcnow()}")
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)

bot.run(TOKEN)
