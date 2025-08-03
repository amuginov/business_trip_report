# filepath: bot/main.py
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.services.database import init_db
from bot.handlers import admin, user, guest, common  # добавьте common

def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(guest.router)
    dp.include_router(common.router)  # регистрация роутера common
    print("Bot started. Polling...")
    dp.run_polling(bot)

if __name__ == "__main__":
    main()