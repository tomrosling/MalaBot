import os
import discord
from dotenv import load_dotenv
from thesaurus import get_synonym
from tts import text_to_mp3
from io import BytesIO

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()
voice_client = None
message_queue = []


def after_play_finished(err):
    # If another message has been queued, play it.
    if message_queue:
        msg = message_queue.pop(0)
        voice_client.play(msg, after=after_play_finished)


async def update_bot_channel(guild):
    global voice_client

    all_channels = await guild.fetch_channels()
    if not all_channels:
        return

    def get_num_members(idx):
        channel = all_channels[idx]
        if isinstance(channel, discord.VoiceChannel):
            if channel == guild.afk_channel:
                return 0
            num_members = len(channel.members)
            if voice_client and voice_client.channel == channel:
                num_members -= 1
            return num_members
        else:
            return 0

    # Find the channel with the most non-bot members and try to join it.
    max_idx = max(range(len(all_channels)), key=lambda i: get_num_members(i))
    if get_num_members(max_idx) > 0:
        channel_to_join = all_channels[max_idx]
        if voice_client:
            if voice_client.channel != channel_to_join:
                await voice_client.move_to(channel_to_join)
        else:
            voice_client = await channel_to_join.connect()
    elif voice_client:
        # Leave voice if there's nobody left on the server.
        await voice_client.disconnect()
        voice_client = None



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_voice_state_update(member, old_state, new_state):
    # Don't send messages about the bot itself!
    if member == client.user:
        return

    # Has the user moved channel?
    new_channel = new_state.channel
    old_channel = old_state.channel
    if old_channel == new_channel:
        return

    # Check if the bot should go to the new channel.
    guild = (old_channel and old_channel.guild) or (new_channel and new_channel.guild)
    assert(guild)
    await update_bot_channel(guild)

    # Build a message based on the change. Treat 'afk' channel as if user disconnected.
    now_in_channel = (new_channel and new_channel != guild.afk_channel)
    was_in_channel = (old_channel and old_channel != guild.afk_channel)
    message = None
    if now_in_channel:
        if was_in_channel:
            message = f'{member.display_name} {get_synonym("moved to")} {new_channel.name}.'
        else:
            message = f'{get_synonym("Hello")} {member.display_name}!'
    elif was_in_channel:
        message = f'{get_synonym("Goodbye")} {member.display_name}!'

    # Send the text-to-speech message, or queue it if the bot is already speaking.
    if message and voice_client:
        audio_stream = discord.PCMAudio(BytesIO(text_to_mp3(message)))
        if voice_client.is_playing():
            message_queue.append(audio_stream)
        else:
            voice_client.play(audio_stream, after=after_play_finished)


client.run(TOKEN)
