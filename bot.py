from telegram.ext import Updater
from bot.handlers import register_handlers
from bot.config import TOKEN
from bot.utils import load_wins

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

register_handlers(dispatcher)

load_wins()

updater.start_polling()
updater.idle()
