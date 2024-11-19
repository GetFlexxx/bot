import logging
from log import blacklist_logger, status_logger, message_logger, delete_logger, rate_logger
from aiohttp.web_routedef import delete

blacklist_logger = logging.getLogger('blacklist_logger')
delete_logger = logging.getLogger('delete_logger')

async def handle_message(message, bot, blacklist):
    for word in blacklist:
        if word in message.content.lower():
            blacklist_logger.warning(f"Blacklist-Wort gefunden in Nachricht von {message.author}: {message.content}")
            await message.delete()
            delete_logger.warning(f"Nachricht von {message.author}: '{message.content}' gelöscht!")
            await message.channel.send(f"{message.author.mention}, deine Nachricht wurde wegen unangemessener Wörter gelöscht.")
            return

    if "hallo" in message.content.lower():
        await message.channel.send(f"Hallo, {message.author.mention}!")

    elif "!hilfe" in message.content.lower():
        await message.channel.send("Was möchtest du wissen? Ich kann dir bei verschiedenen Themen helfen.")

    elif "bye" in message.content.lower():
        await message.channel.send(f"Tschüss, {message.author.mention}!")