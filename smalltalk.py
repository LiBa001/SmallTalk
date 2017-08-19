import discord

import langmanager

client = discord.Client()

LANGUAGES = langmanager.languages
TTS = False
OUTPUT = False


@client.event
async def on_ready():
    print("Logged in as: %s" % client.user.name)
    print("______________%s" % (len(client.user.name) * "_"))


@client.event
async def on_message(message: discord.Message):
    for LANGUAGE in LANGUAGES:
        if message.author.id != client.user.id:
            response = langmanager.get_answer_from_question(message.content, LANGUAGE, OUTPUT)
            try:
                if response is not None:
                    await client.send_message(message.channel, response, tts=TTS)
                    return 0
            except discord.errors.Forbidden:
                pass


client.run("[Bot-Token]")  # TODO insert token
