from aiogram import types
from aiogram.dispatcher import Dispatcher

# Initialize the user handlers
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(report_command, commands=['report'])

async def start_command(message: types.Message):
    await message.answer("Welcome to the Advance Report Bot! Use /help to see available commands.")

async def help_command(message: types.Message):
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/report - Generate an advance report"
    )
    await message.answer(help_text)

async def report_command(message: types.Message):
    await message.answer("Please upload the travel order PDF file.")