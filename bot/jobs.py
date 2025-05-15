# bot/jobs.py

from datetime import datetime
from telegram.ext import CallbackContext
from bot.config import START_DATE
from bot.config import ADMIN_ID


def stage_day_reminder(context: CallbackContext):
    today = datetime.now()
    warsaw_time = today.strftime("%d.%m.%Y — %H:%M")
    day_number = (today.date() - START_DATE.date()).days + 1

    print(f"(4terminalMsge)🧠 Сегодня: {day_number}-й день этапа (от {START_DATE.date()})")

    message = f"Сегодня {warsaw_time} — Варшава — {day_number}-й день второго этапа!\nЧто сегодня реализуешь?"

    # Универсальный способ извлечь chat_id
    chat_id = getattr(context.job, 'chat_id', None) or context.user_data.get("chat_id", ADMIN_ID)

    if chat_id:
        context.bot.send_message(chat_id=chat_id, text=message)
    else:
        print("❌ Не удалось определить chat_id")

    context.user_data["last_stage_day"] = day_number
    print(f"💾 Сохранил в user_data['last_stage_day']: {day_number}")


def pytutor_reminder(context: CallbackContext):
    print("🔔 PyTutor reminder отправлен!")

    chat_id = getattr(context.job, 'chat_id', None) or context.user_data.get("chat_id", ADMIN_ID)

    if chat_id:
        context.bot.send_message(
            chat_id=chat_id,
            text="🧠 Осталось 15 минут! Зайди на https://pythontutor.com и реши хотя бы одну задачу."
        )
    else:
        print("❌ chat_id не найден")


def test_reminder(update, context: CallbackContext):
    context.user_data["chat_id"] = update.effective_chat.id
    stage_day_reminder(context)
    update.message.reply_text("Тестовое напоминание отправлено!")


def test_pytutor(update, context: CallbackContext):
    pytutor_reminder(context)
    update.message.reply_text("Тест PyTutor-напоминания отправлен!")
