# FILE: /advance-report-bot/advance-report-bot/bot/main.py

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from handlers import admin_handlers, user_handlers, guest_handlers
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register handlers
admin_handlers.register_handlers(dp)
user_handlers.register_handlers(dp)
guest_handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)