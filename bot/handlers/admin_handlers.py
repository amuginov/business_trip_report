from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.services.database import Database

db = Database()

async def list_users(message: types.Message):
    users = db.get_all_users()
    user_list = "\n".join([f"{user['surname']} {user['name']} {user['patronymic']}" for user in users])
    await message.answer(f"Список пользователей:\n{user_list}")

async def register_user(message: types.Message):
    await message.answer("Введите фамилию нового пользователя:")
    # Logic to handle user input and registration

async def delete_user(message: types.Message):
    await message.answer("Введите ID пользователя для удаления:")
    # Logic to handle user input and deletion

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(list_users, commands=['users'], state='*')
    dp.register_message_handler(register_user, commands=['new_user'], state='*')
    dp.register_message_handler(delete_user, commands=['delete_user'], state='*')