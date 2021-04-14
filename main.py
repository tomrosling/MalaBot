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
async def on_message(msg):
    if 'malabot' in msg.content.lower():
        await msg.reply('pong?')

@client.event
async def on_voice_state_update(member, old_state, new_state):
    if not text_channel:
        return

    new_channel = new_state.channel
    old_channel = old_state.channel

    # TODO: Iterate members of the channel we joined/left?
    #users = [await client.fetch_user(<REDACTED>)]
    #print(users)
    #for user in users:
    #    await user.send('hey buddy', tts = True) # Apparently tts doesn't work for PMs? :(

    # Flaw: tts only seems to trigger on the active channel, for me at least
    message = None
    if new_channel:
        if old_channel:
            message = f'{member.display_name} {get_synonym('moved to')} {new_channel.name}.'
        else:
            message = f'{member.display_name} {get_synonym('joined')} {new_channel.name}.'
    elif old_channel:
        message = f'{member.display_name} {get_synonym('left')} {old_channel.name}.'

    if message:
        await text_channel.send(message, tts = True, delete_after = 10)


client.run(TOKEN)
