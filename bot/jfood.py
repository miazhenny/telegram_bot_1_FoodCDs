# bot/jfood.py

import json
import os
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackContext
from config import JFOOD_FILE


def load_jfood():
    if os.path.exists(JFOOD_FILE):
        with open(JFOOD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "cooldown_level": 0,
            "last_jfood_date": None
        }


def save_jfood(data):
    with open(JFOOD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_jfood(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠ Укажи дату после команды, например: /add_jfood 01.05.2025")
        return

    try:
        last_date = datetime.strptime(context.args[0], "%d.%m.%Y").date()
    except ValueError:
        update.message.reply_text("❌ Неверный формат даты. Используй ДД.ММ.ГГГГ")
        return

    data = load_jfood()
    data["last_jfood_date"] = last_date.strftime("%Y-%m-%d")
    save_jfood(data)

    cd_days = 30 + data["cooldown_level"]
    next_date = last_date + timedelta(days=cd_days)

    update.message.reply_text(
        f"🍔 Джанкфуд зафиксирован: {last_date.strftime('%d.%m.%Y')}\n"
        f"Кулдаун Lv.{data['cooldown_level']} закончится: {next_date.strftime('%d.%m.%Y')}"
    )


def jfood_cd(update: Update, context: CallbackContext):
    data = load_jfood()

    if not data["last_jfood_date"]:
        update.message.reply_text("🍔 Ты ещё не ел джанкфуд, нет даты!")
        return

    last_date = datetime.strptime(data["last_jfood_date"], "%Y-%m-%d").date()
    cd_days = 30 + data["cooldown_level"]
    next_date = last_date + timedelta(days=cd_days)
    today = datetime.now().date()
    remaining = (next_date - today).days

    if remaining > 0:
        update.message.reply_text(
            f"🍟 Последний джанкфуд: {last_date.strftime('%d.%m.%Y')}\n"
            f"Кулдаун Lv.{data['cooldown_level']} закончится: {next_date.strftime('%d.%m.%Y')}\n"
            f"Осталось {remaining} дней"
        )
    else:
        update.message.reply_text(
            f"✅ Кулдаун пройден! Можно съесть одну порцию джанкфуда! (например, 🌯 шаурма)\n"
            f"Lv.{data['cooldown_level']} закончился ещё {abs(remaining)} дн. назад.\n"
            f"Хочешь повысить уровень кулдауна? Напиши /lvlup_cd"
        )


def lvlup_cd(update: Update, context: CallbackContext):
    data = load_jfood()

    if not data["last_jfood_date"]:
        update.message.reply_text("⚠️ Сначала зафиксируй джанкфуд через /add_jfood")
        return

    last_date = datetime.strptime(data["last_jfood_date"], "%Y-%m-%d").date()
    cd_days = 30 + data["cooldown_level"]
    next_date = last_date + timedelta(days=cd_days)
    today = datetime.today().date()

    if today >= next_date:
        data["cooldown_level"] += 1
        save_jfood(data)
        update.message.reply_text(
            f"🔼 Уровень повышен! Теперь Lv.{data['cooldown_level']} "
            f"— кулдаун = {30 + data['cooldown_level']} дней 💪"
        )
    else:
        days_left = (next_date - today).days
        update.message.reply_text(
           f"⛔ Ещё рано! Осталось {days_left} дней до конца кулдауна."
        )
