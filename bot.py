import os
import json

import discord
from discord.ext import commands, tasks
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv


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

db_reference = db.reference('test/int')
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
    global flag
    print(f"From callback: {flag}")
    flag = True
    # bot.loop.create_task(send_message(bot.get_channel(1101143451564781631), f"This changed {db_reference.get()}"))

@tasks.loop(seconds=0.5)
async def check_flag():
    global flag
    print(f"From loop: {flag}")
    if flag:
        await send_message(bot.get_channel(1101143451564781631), f"This changed {db_reference.get()}")
        flag = False

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

db_reference.listen(on_value_change)
bot.run(TOKEN, reconnect=True)
