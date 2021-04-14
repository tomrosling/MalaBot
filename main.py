import os
import discord
from dotenv import load_dotenv
from thesaurus import get_synonym

load_dotenv()
TOKEN = os.getenv('TOKEN')
text_channel = None
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for c in client.get_all_channels():
        if isinstance(c, discord.TextChannel) and 'malabot' in c.name:
            global text_channel
            text_channel = c
            break

@client.event
async def on_voice_state_update(member, old_state, new_state):
    # If we failed to initialised, give up.
    if not text_channel:
        return

    # Has the user moved channel?
    new_channel = new_state.channel
    old_channel = old_state.channel
    if old_channel == new_channel:
        return

    # Build a message based on the change. Treat 'afk' channel as if user disconnected.
    now_in_channel = (new_channel and new_channel.name.lower() != 'afk')
    was_in_channel = (old_channel and old_channel.name.lower() != 'afk')
    message = None
    if now_in_channel:
        if was_in_channel:
            message = f'{member.display_name} {get_synonym("moved to")} {new_channel.name}.'
        else:
            message = f'{get_synonym("Hello")} {member.display_name}!'
    elif was_in_channel:
        message = f'{get_synonym("Goodbye")} {member.display_name}!'

    # Send the text-to-speech message.
    if message:
        await text_channel.send(message, tts = True, delete_after = 10)


client.run(TOKEN)
