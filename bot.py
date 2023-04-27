import os
import json

import discord
from discord.ext import commands, tasks
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv


users = {
    "25 54 141 93 ": "Waseem",
}

load_dotenv()
firebase_config = json.loads(os.getenv('FIREBASE_CONFIG'))
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://cc-project--2023-default-rtdb.asia-southeast1.firebasedatabase.app/'})
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX,
                   description="Testing the bot", intents=intents)
flag = False
count = 0

db_reference_active = db.reference('active')
db_reference_uid = db.reference('User')

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    check_flag.start()
    

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')
    await bot.get_channel(1101143451564781631).send("This is me again")

async def send_message(channel: discord.TextChannel, message: str):
    await channel.send(message)

def on_value_change(event):
    global count
    if not count:
        count += 1
        return
    global flag
    flag = True

@tasks.loop(seconds=0.5)
async def check_flag():
    global flag
    if flag:
        await send_message(bot.get_channel(1101143451564781631), f"{users[db_reference_uid.get()]} just entered")
        flag = False

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

db_reference_active.listen(on_value_change)
bot.run(TOKEN, reconnect=True)
