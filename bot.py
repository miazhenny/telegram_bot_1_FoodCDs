from telegram.ext import ApplicationBuilder
from bot.handlers import register_handlers
from bot.config import TOKEN
from bot.utils import load_wins

def main():
    """Start the bot using Application.run_polling."""
    application = ApplicationBuilder().token(TOKEN).build()
    register_handlers(application)
    load_wins()
    print("✅ Бот запущен и слушает команды...")
    application.run_polling()

if __name__ == "__main__":
    main()



