async def bot_offline():
    """Bot geht offline."""
    print(f"{bot.user} wurde vom Server getrennt.")

    # Hole den Textkanal 'bot-ready-down'
    channel = discord.utils.get(bot.guilds[0].text_channels, name='bot-ready-down')
    if channel:
        await channel.send(f"{bot.user} ist jetzt OFFLINE.")

atexit.register(bot_offline)

@bot.event
async def on_ready():
    status_logger.warning(f"Bot ist bereit! Eingeloggt als {bot.user}")
    blacklist_logger.info(f"Geladene Blacklist-Wörter: {blacklist}")
    channel = discord.utils.get(bot.guilds[0].text_channels, name='bot-ready-down')
    if channel:
        await channel.send(f"{bot.user} ist jetzt ONLINE!")
    print(f"{bot.user} ist online")