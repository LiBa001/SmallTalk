import discord
import jPoints
import random

client = discord.Client()

@client.event
async def on_ready():
    print(client.user.name)
    print("______________")


@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        themes = ["Begruessungen", "Verabschiedungen","Aktionen", "Laune", "Wetter", "Beleidigung", "Wuensche", "Dank",
                  "Lustig", "Witz", "Freude", "Staunen", "Bot", "Meinung", "Alter", "Farbe", "Langeweile",
                  "Zustimmung", "Ablehnung", "Fragen", "Du"]
        for theme in themes:
            for i in jPoints.chat_data.get(theme+"Fragen"):
                if i in message.content.lower():
                    msg = jPoints.chat_data.get(theme+"Antworten")
                    await client.send_message(message.channel, msg[random.randint(0,len(msg)-1)])
                    return 0


client.run("[Bot-Token]")  #TODO insert token