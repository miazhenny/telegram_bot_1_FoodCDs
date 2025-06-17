# bot/menus.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes


def main_menu(update: Update, context: ContextTypes):
    keyboard = [
        [InlineKeyboardButton("Ценности от Брюса Ли 🥋", callback_data='motivate')],
        [InlineKeyboardButton("Добавить победу дня 🏆", callback_data='add_win')],
        [InlineKeyboardButton("Список побед 📋", callback_data='list_wins')],
        [InlineKeyboardButton("Очистить победы 🗑", callback_data='clear_wins')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an action:', reply_markup=reply_markup)


def inline_buttons(update: Update, context: ContextTypes):
    keyboard = [
        [InlineKeyboardButton("YouTube", callback_data='youtube')],
        [InlineKeyboardButton("GitHub", callback_data='github')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выбери куда пойти:', reply_markup=reply_markup)

    