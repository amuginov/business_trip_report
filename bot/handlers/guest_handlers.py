from aiogram import types
from aiogram.dispatcher import Dispatcher

async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Я бот для генерации авансовых отчетов. Нажмите 'Заявка на регистрацию', чтобы начать.")

async def help_command(message: types.Message):
    help_text = (
        "Я могу помочь вам с регистрацией и предоставлением авансовых отчетов.\n"
        "1. Нажмите 'Заявка на регистрацию', чтобы зарегистрироваться.\n"
        "2. Если у вас есть вопросы, нажмите 'Помощь'."
    )
    await message.answer(help_text)

def register_guest_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(help_command, commands=["help"])