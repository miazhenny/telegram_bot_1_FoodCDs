# bot/handlers.py

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from bot.menus import main_menu, inline_buttons, button_handler
from bot.utils import load_wins, save_wins
from bot.jfood import add_jfood, jfood_cd, lvlup_cd
from bot.jobs import test_reminder, test_pytutor
from bot.config import START_DATE
from data.motivational_quotes import motivational_quotes
from bot.config import ADMIN_ID


def start(update: Update, context: CallbackContext):
    print("⚙️ Запущена команда /start")
    update.message.reply_text("I am your personal motivation coach! 🚀")

    context.user_data["chat_id"] = update.effective_chat.id
    chat_id = update.effective_chat.id

    main_menu(update, context)


def motivate(update: Update, context: CallbackContext):
    from random import choice
    quote = choice(motivational_quotes)
    update.message.reply_text(quote)


def creator(update: Update, context: CallbackContext):
    update.message.reply_text("Created by Snakedog")


def info(update: Update, context: CallbackContext):
    update.message.reply_text("Я мотиватор-бот. Я умею мотивировать тебя, рассказывать о себе и поддерживать твой настрой!")


def picture(update: Update, context: CallbackContext):
    with open("1_onYT.png", 'rb') as photo:
        update.message.reply_photo(photo, caption="nevagivup!")


def video(update: Update, context: CallbackContext):
    with open('files/video.mp4', 'rb') as vid:
        update.message.reply_video(vid, caption="я жду твой новый трек! Ты поставил цель выпускать трек каждую неделю! Я помню, и не дам забыть тебе!")


wins = []  # локальный список побед

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if context.user_data.get("waiting_for_win"):
        wins.append(update.message.text)
        save_wins()
        update.message.reply_text("Победа сохранена! 💪")
        context.user_data["waiting_for_win"] = False
        return

    if "привет" in text:
        update.message.reply_text("Привет! Рад тебя видеть! 🚀")
    elif "пока" in text:
        update.message.reply_text("До встречи, друг! 👋")
    elif "как дела" in text:
        update.message.reply_text("Отлично! Программируем и растём! А у тебя как?")
    else:
        update.message.reply_text("Не понял тебя сейчас. Вот меню:")
        main_menu(update, context)


def mood(update: Update, context: CallbackContext):
    mood = " ".join(context.args)
    context.user_data["mood"] = mood
    update.message.reply_text(f"🧠 Настроение сохранено: {mood}")


def remind_on(update: Update, context: CallbackContext):
    from datetime import time
    from bot.jobs import stage_day_reminder, pytutor_reminder

    chat_id = context.user_data.get("chat_id")
    if not chat_id:
        chat_id = ADMIN_ID
        context.bot.send_message(chat_id=chat_id, text="❗ Пожалуйста, запусти /start сначала, чтобы я мог с тобой работать.")
        return

    job_queue = context.job_queue

    job_queue.run_daily(
        stage_day_reminder,
        time(hour=4, minute=0),
        context=chat_id,
        name=str(chat_id)
    )

    job_queue.run_daily(
        pytutor_reminder,
        time=time(hour=8, minute=15),
        context=chat_id
    )

    job_queue.run_daily(
        pytutor_reminder,
        time=time(hour=19, minute=15),
        context=chat_id
    )

    update.message.reply_text("⏰ Напоминания активированы!")


def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("motivate", motivate))
    dispatcher.add_handler(CommandHandler("creator", creator))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("picture", picture))
    dispatcher.add_handler(CommandHandler("video", video))
    dispatcher.add_handler(CommandHandler("add_jfood", add_jfood))
    dispatcher.add_handler(CommandHandler("jfood_cd", jfood_cd))
    dispatcher.add_handler(CommandHandler("lvlup_cd", lvlup_cd))
    dispatcher.add_handler(CommandHandler("mood", mood))
    dispatcher.add_handler(CommandHandler("test_reminder", test_reminder))
    dispatcher.add_handler(CommandHandler("test_pytutor", test_pytutor))
    dispatcher.add_handler(CommandHandler("remind_on", remind_on))
    dispatcher.add_handler(CommandHandler("menu", main_menu))
    dispatcher.add_handler(CommandHandler("links", inline_buttons))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
