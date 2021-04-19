import os
import discord
from dotenv import load_dotenv
from thesaurus import get_synonym
from tts import text_to_pcm
from io import BytesIO

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()
voice_client = None
message_queue = []


def after_play_finished(err):
    global message_queue

    # If another message has been queued, play it.
    if voice_client:
        if message_queue:
            msg = message_queue.pop(0)
            voice_client.play(msg, after=after_play_finished)
    else:
        message_queue = []


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
            num_members = len(channel.voice_states)
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
            # NOTE: VoiceChannel.connect() seems to be the only way to create a VoiceClient,
            # but we need to pass the same channel again to Guild.change_voice_state() to self-deafen,
            # otherwise we'll be disconnected.            
            voice_client = await channel_to_join.connect()
            await guild.change_voice_state(channel=channel_to_join, self_deaf=True)
    elif voice_client:
        # Leave voice if there's nobody left on the server.
        await voice_client.disconnect()
        voice_client = None



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_voice_state_update(member, old_state, new_state):
    # Don't send messages about ourself or any other bots!
    if member.bot:
        return

    # Has the user moved channel?
    new_channel = new_state.channel
    old_channel = old_state.channel
    if old_channel == new_channel:
        return

    # Check if the bot needs to change channel.
    guild = (old_channel and old_channel.guild) or (new_channel and new_channel.guild)
    assert(guild)
    await update_bot_channel(guild)
    if not voice_client:
        return

    # Build a message based on the change. Treat 'afk' channel as if user disconnected.
    message = None
    lang = None
    if new_channel == voice_client.channel:
        lang, hello = get_synonym('Hello')
        message = f'{hello} {member.display_name}!'
    elif old_channel == voice_client.channel:
        lang, goodbye = get_synonym('Goodbye')
        message = f'{goodbye} {member.display_name}!'

    if member.display_name == 'James':
        message = message + ' we were so worried!'

    # Send the text-to-speech message, or queue it if the bot is already speaking.
    if message and voice_client:
        audio_stream = discord.PCMAudio(BytesIO(text_to_pcm(message)))
        if voice_client.is_playing():
            message_queue.append(audio_stream)
        else:
            voice_client.play(audio_stream, after=after_play_finished)


client.run(TOKEN)
