# bot/utils.py

import json
import os
import random
from bot.config import WINS_FILE
from bot.data.motivational_quotes import motivational_quotes


wins = []  # Глобальный список побед
available_quotes = motivational_quotes.copy()  # Для уникальной ротации


def load_wins():
    global wins
    if os.path.exists(WINS_FILE):
        with open(WINS_FILE, "r", encoding="utf-8") as f:
            wins = json.load(f)
    else:
        wins = []


def save_wins():
    with open(WINS_FILE, "w", encoding="utf-8") as f:
        json.dump(wins, f, ensure_ascii=False, indent=2)


def get_unique_quote():
    global available_quotes
    if not available_quotes:
        available_quotes = motivational_quotes.copy()
    quote = random.choice(available_quotes)
    available_quotes.remove(quote)
    return quote
