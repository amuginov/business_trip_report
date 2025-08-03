from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def guest_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Заявка на регистрацию")],
            [KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True
    )