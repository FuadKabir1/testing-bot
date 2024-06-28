import discord
import json
import os
import requests
import random
from dotenv import load_dotenv
from replit import db
load_dotenv()

token = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.all())

#------------------------------------------------------------#

sad_words = [
    'sad', 'depressing', 'depression', 'unhappy', 'miserable', 'angry'
]

starter_encouragements = [
    'cheer up!', 'hang in there', 'you are a great person'
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_dt = json.loads(response.text)
    quote = json_dt[0]['q'] + " -" + json_dt[0]['a']
    return quote


# def get_quote_image():
#     response = requests.get("https://zenquotes.io/api/image")
# quote = json.loads(response.text)[0]['i']
#     return quote


def update_encouragements(encouraging_message):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements
    

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if (message.author == client.user):
        return

    msg = message.content

    if (message.content.startswith('$hello')):
        await message.channel.send('Hi!')

    if (message.content.startswith('ah!')):
        await message.channel.send("cdi na")

    if (message.content.startswith('$inspire')):
        quote = get_quote()
        await message.channel.send(quote)

    if(any(word in msg for word in sad_words)):
        await message.channel.send(random.choice(starter_encouragements))

    if(msg.startswith("$new")):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New message added successfully")

    if(msg.startswith("$del ")):
        encouragements = []
        if ("encouragements" in db.keys()):
            index = int(msg.split("$del",1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send("Delete Successfully")

    if(msg.startswith("$list")):
        encouragements = []
        if('encouragements' in db.keys()):
            encouragements = db['encouragements']
        await message.channel.send(f'[{", ".join(encouragements)}]')
client.run(token)
