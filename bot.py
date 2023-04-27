import os
import json

import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv


load_dotenv()
firebase_config = json.loads(os.getenv('FIREBASE_CONFIG'))
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')


cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://cc-project--2023-default-rtdb.asia-southeast1.firebasedatabase.app/'})

bot = commands.Bot(command_prefix=PREFIX,
                   description="Testing the bot", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready')

# @bot.command()
# async def ping(ctx):
     
bot.run(TOKEN, reconnect=True)
