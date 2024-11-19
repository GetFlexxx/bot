import logging
import os

# Stelle sicher, dass der Logs-Ordner existiert
os.makedirs("logs", exist_ok=True)

# Funktion zum Erstellen eines Loggers
def setup_logger(name, log_file, level=logging.INFO, formatter=None):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    if formatter is None:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

# Logger für Blacklist
blacklist_logger = setup_logger(
    "blacklist_logger",
    "logs/blacklist.log",
    logging.WARNING
)

# Logger für Bot-Status (Start, Stop, Fehler)
status_logger = setup_logger(
    "status_logger",
    "logs/bot_status.log",
    logging.INFO
)

# Logger für Nachrichten
message_logger = setup_logger(
    "message_logger",
    "logs/messages.log",
    logging.INFO
)

# Logger für gelöschte Nachrichten
delete_logger = setup_logger(
    "delete_logger",
    "logs/delete.log",
    logging.WARNING
)

rate_logger = setup_logger(
    "rate_logger",
    "logs/ratespiel.log",
    logging.WARNING
)