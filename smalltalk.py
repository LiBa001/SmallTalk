import discord
import sqlib
import langmanager
import json

client = discord.Client()

LANGUAGES = langmanager.languages
OUTPUT = False


def add_server(server_id):
    sqlib.servers.add_element(server_id, {'prefix': 'ST', 'channels': '{}', 'language': 'all'})


@client.event
async def on_ready():
    print("Logged in as: %s" % client.user.name)
    print("______________%s" % (len(client.user.name) * "_"))

    await client.change_presence(game=discord.Game(name="SThelp"))

    for server in client.servers:
        if sqlib.servers.get(server.id) is None:
            add_server(server.id)


@client.event
async def on_message(message: discord.Message):
    if sqlib.servers.get(message.server.id) is None:
        add_server(message.server.id)
    prefix = sqlib.servers.get(message.server.id, 'prefix')[0]

    channels_str = sqlib.servers.get(message.server.id, 'channels')[0]
    channels_dict = json.loads(channels_str)

    if channels_dict[message.channel.id] == 2:
        TTS = True
    else:
        TTS = False

    content = message.content.split(' ')
    if len(content) > 1:
        content = content[1]
    else:
        content = content[0]

    if message.content.startswith(prefix + 'start'):
        if content.lower() == 'tts':
            channels_dict[message.channel.id] = 2
            TTS = True
        else:
            channels_dict[message.channel.id] = 1
        channels_str = json.dumps(channels_dict)
        sqlib.servers.update(message.server.id, {'channels': channels_str})
        await client.send_message(message.channel,
                                  langmanager.random_topic_answer('greetings', LANGUAGES[0]),
                                  tts=TTS)
        return 0

    elif message.content.startswith(prefix + 'stop'):
        if content.lower() == 'tts' and TTS:
            channels_dict[message.channel.id] = 1
            TTS = False
            await client.send_message(message.channel, "TTS OFF")
        elif channels_dict[message.channel.id] >= 1:
            channels_dict[message.channel.id] = 0
            await client.send_message(message.channel,
                                      langmanager.random_topic_answer('leaving', LANGUAGES[0]),
                                      tts=TTS)
        channels_str = json.dumps(channels_dict)
        sqlib.servers.update(message.server.id, {'channels': channels_str})
        return 0

    elif message.content.startswith(prefix + 'help'):
        help_msg = discord.Embed(
            title="Help",
            description="Commands to manage the conversation.",
            color=0xff4000
        )
        help_msg.add_field(
            name=prefix + 'start',
            value="Starts the conversation.\n"
                  "Type: `{prefix}start TTS` to activate text to speech.\n"
                  "Mind that the bot needs the permissions to do so.".format(prefix=prefix)
        )
        help_msg.add_field(
            name=prefix + 'stop',
            value="Ends the conversation.\n"
                  "Type: '{prefix}stop TTS' to only deactivate text to speech.\n".format(prefix=prefix)
        )

        await client.send_message(message.channel, embed=help_msg)
        return 0

    elif message.channel.id not in channels_dict:
        channels_dict[message.channel.id] = 0
        channels_str = json.dumps(channels_dict)
        sqlib.servers.update(message.server.id, {'channels': channels_str})

    if channels_dict[message.channel.id] >= 1:
        for LANGUAGE in LANGUAGES:
            if message.author.id != client.user.id:
                response = langmanager.get_answer_from_question(message.content, LANGUAGE, OUTPUT)
                try:
                    if response is not None:
                        await client.send_message(message.channel, response, tts=TTS)
                        return 0
                except discord.errors.Forbidden:
                    pass


@client.event
async def on_server_join(server):
    if sqlib.servers.get(server.id) is None:
        add_server(server.id)


client.run("[Bot-Token]")  # TODO insert token
