# main.py

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_commands():

    for folder in os.listdir("./commands"):

        folder_path = f"./commands/{folder}"

        if os.path.isdir(folder_path):

            for file in os.listdir(folder_path):

                if file.endswith(".py") and file != "__init__.py":

                    extension = f"commands.{folder}.{file[:-3]}"
                    await bot.load_extension(extension)

@bot.event
async def on_ready():

    print(f"Bot online: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash commands sincronizados")

    except Exception as e:
        print(e)

async def main():
    async with bot:

        await load_commands()
        await bot.start(token)

asyncio.run(main())