import discord
from aiohttp.web_routedef import delete
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import atexit
from responses import handle_message
import random
from rategame import start_game, guess_number
from discord.ext import commands
from log import blacklist_logger, status_logger, message_logger, delete_logger, rate_logger

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def load_blacklist():
    try:
        with open("blacklist.txt", "r") as file:
            blacklist_logger.error("Blacklist wurde geladen")
            return [line.strip().lower() for line in file.readlines()]
        blacklist_logger.error("Blacklist wurde geladen")
    except FileNotFoundError:
        blacklist_logger.error("Die Datei 'blacklist.txt' wurde nicht gefunden!")
        return []

blacklist = load_blacklist()

@bot.event
async def bot_offline():
    status_logger.warning(f"Bot ist Offline!")
    print(f"{bot.user} wurde vom Server getrennt.")

atexit.register(bot_offline)

@bot.event
async def on_ready():
    status_logger.warning(f"Bot ist bereit! Eingeloggt als {bot.user}")
    blacklist_logger.info(f"Geladene Blacklist-Wörter: {blacklist}")
    channel = discord.utils.get(bot.guilds[0].text_channels, name='bot-ready-down')
    if channel:
        await channel.send(f"{bot.user} ist jetzt ONLINE!")
    print(f"{bot.user} ist online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_logger.warning(f"Nachricht von {message.author}: {message.content}")

    await handle_message(message, bot, blacklist)

    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    status_logger.error(f"Fehler aufgetreten: {event}")
    print(f"Fehler aufgetreten: {event}")

@bot.command()
async def erraten(ctx):
    """Startet das Zahlenspiel."""
    await start_game(ctx)

# Befehl zum Raten der Zahl
@bot.command()
async def rate(ctx, zahl: int):
    """Überprüft die geratene Zahl."""
    await guess_number(ctx, zahl)

@bot.command()
async def punkte(ctx):
    """Zeigt die Punkte des Benutzers an."""
    from rategame import show_points
    await show_points(ctx)


@bot.command()
async def punkte_speichern(ctx):
    """Speichert die Punkte manuell."""
    from rategame import save_points
    save_points()
    await ctx.send("Punkte wurden erfolgreich gespeichert!")


@bot.command()
async def punkte_laden(ctx):
    """Lädt die Punkte manuell."""
    from rategame import load_points
    load_points()
    await ctx.send("Punkte wurden erfolgreich geladen!")

@bot.command()
async def points(ctx):
    """Zeigt die Punkte des Benutzers an."""
    from rategame import show_points
    await show_points(ctx)

bot.run(TOKEN)