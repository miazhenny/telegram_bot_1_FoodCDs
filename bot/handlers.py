# bot/handlers.py

from telegram import Update
from telegram.ext import ContextTypes

from telegram.ext import CommandHandler, MessageHandler,CallbackQueryHandler
from telegram.ext import filters



from bot.menus import main_menu, inline_buttons
from bot.utils import load_wins, save_wins
from bot.jfood import add_jfood, jfood_cd, lvlup_cd
from bot.jobs import test_reminder, test_pytutor
from bot.config import START_DATE
from data.motivational_quotes import motivational_quotes
from bot.config import ADMIN_ID

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # print("⚙️ Запущена команда /start")
    # await update.message.reply_text("I am your personal motivation coach! 🚀")
    # context.user_data["chat_id"] = update.effective_chat.id
    # chat_id = update.effective_chat.id
    # main_menu(update, context)

     await update.message.reply_text("Привет! Я живой.")


async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from random import choice
    quote = choice(motivational_quotes)
    await update.message.reply_text(quote)


async def creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Created by Snakedog")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я мотиватор-бот. Я умею мотивировать тебя, рассказывать о себе и поддерживать твой настрой!")


async def picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("1_onYT.png", 'rb') as photo:
        await update.message.reply_photo(photo, caption="nevagivup!")


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('files/video.mp4', 'rb') as vid:
       await update.message.reply_video(vid, caption="я жду твой новый трек! Ты поставил цель выпускать трек каждую неделю! Я помню, и не дам забыть тебе!")


wins = []  # локальный список побед

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await update.message.text.lower()

    if context.user_data.get("waiting_for_win"):
        wins.append(update.message.text)
        save_wins()
        await update.message.reply_text("Победа сохранена! 💪")
        context.user_data["waiting_for_win"] = False
        return

    if "привет" in text:
        await update.message.reply_text("Привет! Рад тебя видеть! 🚀")
    elif "пока" in text:
        await update.message.reply_text("До встречи, друг! 👋")
    elif "как дела" in text:
       await update.message.reply_text("Отлично! Программируем и растём! А у тебя как?")
    else:
        await update.message.reply_text("Не понял тебя сейчас. Вот меню:")
        main_menu(update, context)


async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mood = " ".join(context.args)
    context.user_data["mood"] = mood
    await update.message.reply_text(f"🧠 Настроение сохранено: {mood}")


async def remind_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text("⏰ Напоминания активированы!")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()  

    data = query.data

    if data == 'jfood_lvlup':
        query.edit_message_text("Ты поднял уровень джанк-кулдауна! 🔥")
        # вызов функции lvlup_cd() отсюда — если она импортирована

    elif data == 'kill_habit_done':
        query.edit_message_text("Хорош! Один день побеждаешь вредную привычку! ✅")

    else:
        query.edit_message_text("Неизвестное действие.")


async def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("motivate", motivate))
    application.add_handler(CommandHandler("creator", creator))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("picture", picture))
    application.add_handler(CommandHandler("video", video))
    application.add_handler(CommandHandler("add_jfood", add_jfood))
    application.add_handler(CommandHandler("jfood_cd", jfood_cd))
    application.add_handler(CommandHandler("lvlup_cd", lvlup_cd))
    application.add_handler(CommandHandler("mood", mood))
    application.add_handler(CommandHandler("test_reminder", test_reminder))
    application.add_handler(CommandHandler("test_pytutor", test_pytutor))
    application.add_handler(CommandHandler("remind_on", remind_on))
    application.add_handler(CommandHandler("menu", main_menu))
    application.add_handler(CommandHandler("links", inline_buttons))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^jfood_'))

