import random
import asyncio
from log import blacklist_logger, status_logger, message_logger, delete_logger, rate_logger

# Globale Variablen für das Spiel und Punkte
game_state = {
    "active": False,
    "number": None,
    "attempts": 0,
    "points": {},  # Punkte pro Benutzer
    "timeout_task": None,  # Task für Zeitlimit
}
TIME_LIMIT = 60  # Zeitlimit in Sekunden

async def start_game(ctx):
    """Startet das Zahlenspiel mit Zeitlimit."""
    if game_state["active"]:
        await ctx.send("Es läuft bereits ein Spiel! Rate die Zahl.")
        return

    # Wähle eine Zufallszahl
    game_state["number"] = random.randint(1, 25)
    game_state["active"] = True
    game_state["attempts"] = 0

    await ctx.send(
        f"Ich habe eine Zahl zwischen 1 und 25 ausgewählt. "
        f"Du hast {TIME_LIMIT} Sekunden Zeit, sie zu erraten! Gib deine Tipps mit `!rate <zahl>` ein."
    )

    # Starte das Zeitlimit
    game_state["timeout_task"] = asyncio.create_task(end_game_due_to_timeout(ctx))


async def guess_number(ctx, zahl: int):
    """Überprüft die geratene Zahl."""
    if not game_state["active"]:
        await ctx.send("Es läuft gerade kein Spiel. Starte ein neues Spiel mit `!erraten`.")
        return

    game_state["attempts"] += 1

    if zahl < game_state["number"]:
        await ctx.send("Die Zahl ist größer. Versuch's nochmal!")
    elif zahl > game_state["number"]:
        await ctx.send("Die Zahl ist kleiner. Versuch's nochmal!")
    else:
        # Spieler hat die Zahl erraten
        await ctx.send(
            f"Glückwunsch, {ctx.author.name}! Du hast die Zahl {game_state['number']} "
            f"nach {game_state['attempts']} Versuchen erraten!"
        )
        rate_logger.warning(f"{ctx.author.name} hat die Zahl {game_state['number']}, nach {game_state['attempts']} Versuchen erraten. Gesamt Punkte: ")

        # Punkte berechnen und vergeben
        points = calculate_points(game_state["attempts"])
        update_points(ctx.author.name, points)
        await ctx.send(f"Du hast {points} Punkte erhalten! Gesamte Punkte: {game_state['points'][ctx.author.name]}")

        # Spiel zurücksetzen
        await reset_game()


async def end_game_due_to_timeout(ctx):
    """Beendet das Spiel, wenn das Zeitlimit erreicht ist."""
    await asyncio.sleep(TIME_LIMIT)
    if game_state["active"]:
        await ctx.send(
            f"⏳ Zeit ist abgelaufen! Du hast die Zahl {game_state['number']} nicht erraten. Spiel beendet!"
        )
        rate_logger.warning(f"{ctx.author.name} hat die Zahl {game_state['number']} in {game_state['attempts']} Versuchen nicht erraten. Gesamt Punkte: ")
        await reset_game()


async def reset_game():
    """Setzt das Spiel zurück."""
    game_state["active"] = False
    game_state["number"] = None
    game_state["attempts"] = 0
    if game_state["timeout_task"]:
        game_state["timeout_task"].cancel()
        game_state["timeout_task"] = None


def calculate_points(attempts):
    """Berechnet Punkte basierend auf der Anzahl der Versuche."""
    if attempts <= 3:
        return 10
    elif attempts <= 6:
        return 5
    else:
        return 2


def update_points(player, points):
    """Aktualisiert die Punkte des Spielers."""
    if player not in game_state["points"]:
        game_state["points"][player] = 0
    game_state["points"][player] += points


async def show_points(ctx):
    """Zeigt die Punkte des Spielers an."""
    player = ctx.author.name
    points = game_state["points"].get(player, 0)
    await ctx.send(f"🪙 {player}, du hast insgesamt {points} Punkte.")
