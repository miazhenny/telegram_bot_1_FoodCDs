from telegram.ext import ApplicationBuilder
from bot.handlers import register_handlers
from bot.config import TOKEN
from bot.utils import load_wins
import asyncio

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    await register_handlers(application)
    load_wins()
    print("✅ Бот запущен и слушает команды...")
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()



